var t = '';
var button_label = 'PERSON';
var last = null;
window.addEventListener("mouseup", gText);

function removeTag(elementid) {
  var button = document.getElementById(elementid);
  var sentence = document.getElementById("sentence");
  // console.log(element);
  var label = button.parentNode;
  var highlight = label.parentNode;
  console.log(sentence.childNodes.length);
  console.log(highlight.childNodes.length);
  // I need to find a way to handle the count and figure out when it is the last toke to use append instead of insertBefore
  var k = 0;
  for (k += parseInt(highlight.childNodes.length) - 1; k > -1; k--) {
    console.log(k);
    console.log(highlight.childNodes[k]);
    console.log(highlight.childNodes[k].name);
    var i;
    for (i = 0; i < sentence.childNodes.length; i++) {
      if (parseInt(sentence.childNodes[i].id) == (parseInt(highlight.childNodes[k].id) + 1)) {
        console.log(sentence.childNodes[i].id);
        sentence.insertBefore(highlight.childNodes[k], sentence.childNodes[i]);
        break;
      }
    }
  }
  label.remove();
  highlight.remove();
  button.remove();
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

function gText() {
  getLabel();
  var t = window.getSelection();
  if (!t.isCollapsed) {
    var n = t.getRangeAt(0),
      o = n.endContainer.parentElement,
      i = parseInt(n.startContainer.parentElement.getAttribute("id")),
      a = parseInt(o.getAttribute("id"));
    var create_wrapper = '';
    if (i == a) {
      create_wrapper = "#" + String(i);
      $(create_wrapper).wrap('<mark class="label_highlight"></mark>');
      last = i;
    } else {

      while (i <= a) {
        create_wrapper += "#" + String(i) + ", ";
        last = i;
        i++;
      }
      create_wrapper = create_wrapper.replace(/,\s$/g, '');
      $(create_wrapper).wrapAll('<mark class="label_highlight"></mark>');
    }
    if (last != null) {
      $('<span class="label_text">' + String(button_label) + '<span class="xbutton" id="after_' + String(last) + '_button" onclick="removeTag(this.id)">×</span></span>').insertAfter('#' + String(last));
    }
  }
  // this shouldnt be necessary but on some browsers it marks the wrong content
  t = null;
}