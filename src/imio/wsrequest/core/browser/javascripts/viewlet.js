var ws_get_response_container = function(link) {
  var uid = link.attr('uid');
  return link.parent().find('#ws-response-' + uid);
}

var ws_do_request = function() {
  var obj, uid;
  uid = jQuery(this).attr('uid');
  obj = ws_get_response_container(jQuery(this));

  jQuery.ajax({
    url: jQuery(this).attr('request_href'),
    success: function(data) {
      if(data.error != null || data.success == false) {
        ws_set_error(obj);
      } else {
        obj.html('in progress...');
        setTimeout(ws_check_response, 1000, obj, data.id, uid);
      }
    },
    error: function(data) {
      ws_set_error(obj);
    }
  });
  return false;
}

var ws_set_error = function(obj) {
  obj.html('An error occured during the process');
}

var ws_check_response = function(obj, id, uid) {
  jQuery.ajax({
    url: jQuery('#ws-request-' + uid).attr('response_href') + '?id=' + id,
    success: function(data) {
      if(data.success == false && data.error == null) {
        setTimeout(ws_check_response, 2000, obj, id);
      } else if(data.success == true) {
        obj.html('Config synced !');
      } else {
        ws_set_error(obj);
      }
    },
    error: function(data) {
      ws_set_error(obj);
    }
  });
}
