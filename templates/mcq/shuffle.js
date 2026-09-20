function wset3ShuffleChoices(reveal) {
  function run() {
    var box = document.querySelector(".choices");
    if (!box) {
      return;
    }
    var nodes = box.querySelectorAll(".choice");
    var n = nodes.length;
    if (!n) {
      return;
    }
    var key = "wset3-mcq:" + (box.getAttribute("data-card") || "");
    var order = reveal ? wset3LoadOrder(key, n) : wset3NewOrder(n);
    if (!reveal) {
      wset3SaveOrder(key, order);
    }
    wset3ApplyOrder(box, order);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    setTimeout(run, 0);
  }
}

function wset3NewOrder(n) {
  var order = [];
  var i;
  for (i = 0; i < n; i++) {
    order.push(i);
  }
  for (i = n - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = order[i];
    order[i] = order[j];
    order[j] = tmp;
  }
  return order;
}

function wset3SaveOrder(key, order) {
  var raw = JSON.stringify(order);
  try {
    sessionStorage.setItem(key, raw);
  } catch (e) {}
  try {
    localStorage.setItem(key, raw);
  } catch (e) {}
}

function wset3LoadOrder(key, n) {
  var raw = null;
  try {
    raw = sessionStorage.getItem(key);
  } catch (e) {}
  if (!raw) {
    try {
      raw = localStorage.getItem(key);
    } catch (e) {}
  }
  try {
    var order = JSON.parse(raw);
    if (order && order.length === n) {
      return order;
    }
  } catch (e) {}
  return wset3Identity(n);
}

function wset3Identity(n) {
  var order = [];
  for (var i = 0; i < n; i++) {
    order.push(i);
  }
  return order;
}

function wset3ApplyOrder(box, order) {
  var letters = "ABCDEFGHIJ";
  var byId = {};
  var nodes = box.querySelectorAll(".choice");
  var i;
  for (i = 0; i < nodes.length; i++) {
    byId[nodes[i].getAttribute("data-i")] = nodes[i];
  }
  for (i = 0; i < order.length; i++) {
    var el = byId[String(order[i])];
    if (el) {
      box.appendChild(el);
    }
  }
  nodes = box.querySelectorAll(".choice");
  for (i = 0; i < nodes.length; i++) {
    var letter = nodes[i].querySelector(".letter");
    if (letter) {
      letter.textContent = letters.charAt(i);
    }
  }
}
