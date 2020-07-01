var t = '';
var button_label = 'PERSON';
var last = null;
var tag_dictionary = {};
var sentence_id = null;
// window.addEventList("mouseup", gText);

function listenReset() {
  window.addEventListener("mouseup", gText);
  t = '';
}
listenReset();

function post() {
  url = "/";
  method = "post";
  // Create the form object
  var form = document.createElement("form");
  form.setAttribute("method", method);
  form.setAttribute("action", url);
  const hiddenField = document.createElement("input");
  hiddenField.setAttribute("type", "hidden");
  hiddenField.setAttribute("name", "sentence_id");
  hiddenField.setAttribute("value", sentence_id);
  form.appendChild(hiddenField);
  // For each key-value pair
  for (key in tag_dictionary) {
    const hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", key);
    hiddenField.setAttribute("value", tag_dictionary[key]);
    form.appendChild(hiddenField);
  }
  document.body.appendChild(form); // inject the form object into the body section
  form.submit();
}


function removeTag(elementid) {
  var button = document.getElementById(elementid);
  var sentence = document.getElementById("sentence");
  var highlight = button.parentNode;
  var start = null;
  var end = null;
  var label_type = null;
  for (var m = 0; m < highlight.childNodes.length; m++) {
    if (highlight.childNodes[m].id == "label") {
      label_type = String(highlight.childNodes[m].textContent);
      label_remove = highlight.childNodes[m];
    } else if (highlight.childNodes[m].id != null && highlight.childNodes[m].id != "") {
      if (start == null) {
        start = parseInt(highlight.childNodes[m].id)
        end = parseInt(highlight.childNodes[m].id)
      }
      if (parseInt(highlight.childNodes[m].id) > end) {
        end = parseInt(highlight.childNodes[m].id)
      }
    }
  }
  console.log("removing", end)
  $(document).ready(function() {
    $("#label_highlight_" + String(end) + " span").unwrap();
  });
  try {
    label_remove.remove();
    button.remove();
    // highlight.remove();
  } catch (e) {}
  try {
    var index_rem = tag_dictionary[label_type].indexOf(start + ":" + end);
    if (index_rem > -1) {
      tag_dictionary[label_type].splice(index_rem, 1);
    }
  } catch (e) {}
  console.log(tag_dictionary);
}

function getLabel() {
  var ele = document.getElementsByName('label');
  for (i = 0; i < ele.length; i++) {
    if (ele[i].checked) {
      button_label = String(ele[i].id);
      break;
    }
  }
}

function initialLabels() {
  for (var key in tag_dictionary) {
    var local_label = key;
    for (var val in tag_dictionary[key]) {
      var last = null;
      var i = null;
      var a = null;
      var create_wrapper = '';
      i = parseInt(tag_dictionary[key][val].split(":")[0]);
      a = parseInt(tag_dictionary[key][val].split(":")[1]);
      console.log(local_label)
      if (i == a) {
        create_wrapper = "#" + String(i);
        last = i;
        $(create_wrapper).wrap('<mark class="label_highlight ' + String(local_label) + '" id="label_highlight_' + String(last) + '"></mark>');
      } else {
        while (i <= a) {
          create_wrapper += "#" + String(i) + ", ";
          last = i;
          i++;
        }
        create_wrapper = create_wrapper.replace(/,\s$/g, '');
        $(create_wrapper).wrapAll('<mark class="label_highlight ' + String(local_label) + '" id="label_highlight_' + String(last) + '"></mark>');
      }
      var good_selection = false;
      if (i != null && a != null && i != "NaN" && a != "NaN") {
        good_selection = true;
      }
      if (last != null && good_selection == true) {
        $('<span class="label_text" id="label">' + String(local_label) +
          '</span><span class="xbutton" id="after_' + String(last) + '_button" onclick="removeTag(this.id)">x</span>').insertAfter('#' + String(last));
      }
    }
  }
}

function gText() {
  getLabel();
  var start = null;
  var end = null;
  var t = window.getSelection();
  if (!t.isCollapsed) {
    var n = t.getRangeAt(0),
      o = n.endContainer.parentElement,
      i = parseInt(n.startContainer.parentElement.getAttribute("id")),
      a = parseInt(o.getAttribute("id"));
    var create_wrapper = '';
    if (i == a) {
      create_wrapper = "#" + String(i);
      last = i;
      $(create_wrapper).wrap('<mark id="label_highlight_' + String(last) + '" class="label_highlight ' + String(button_label) + '"></mark>');
      start = i;
      end = i;
    } else {
      start = i;
      while (i <= a) {
        create_wrapper += "#" + String(i) + ", ";
        last = i;
        i++;
      }
      end = i - 1;
      create_wrapper = create_wrapper.replace(/,\s$/g, '');
      $(create_wrapper).wrapAll('<mark id="label_highlight_' + String(last) + '" class="label_highlight ' + String(button_label) + '"></mark>');
    }
    var good_selection = false;
    if (start != null && end != null && start != NaN && end != NaN && start + ":" + end != "NaN:NaN" && end >= start) {
      good_selection = true;
      var exists = false;
      for (var key in tag_dictionary) {
        if (key == button_label) {
          exists = true;
          break;
        }
      }
      if (exists == true) {
        tag_dictionary[button_label].push(start + ":" + end);
      } else {
        tag_dictionary[button_label] = [start + ":" + end];
      }
    }
    if (last != null && good_selection == true) {
      $('<span class="label_text" id="label">' + String(button_label) +
        '</span><span class="xbutton" id="after_' + String(last) + '_button" onclick="removeTag(this.id)">x</span>').insertAfter('#' + String(last));
    }
  }
  console.log(tag_dictionary);
  listenReset();
}