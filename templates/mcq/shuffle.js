function wset3ShuffleChoices(reveal) {
  wset3WhenReady(function (box) {
    var nodes = box.querySelectorAll(".choice");
    var n = nodes.length;
    if (!n) {
      return;
    }
    var key = "wset3-mcq:" + (box.getAttribute("data-card") || "");
    var order = reveal ? wset3LoadOrder(key, n) : wset3NewOrder(n, key);
    if (!reveal) {
      wset3SaveOrder(key, order);
    }
    wset3ApplyOrder(box, order);
    if (reveal) {
      wset3MarkPick(box, wset3LoadPick(key));
    } else {
      wset3EnablePicks(box, key);
    }
  });
}

function wset3WhenReady(fn) {
  var tries = 0;
  function tick() {
    var box = document.querySelector(".choices");
    if (box) {
      fn(box);
      return;
    }
    if (tries++ < 40) {
      setTimeout(tick, 50);
    }
  }
  tick();
}

function wset3NewOrder(n, key) {
  var seeded = wset3DroidOrder(n);
  if (seeded) {
    return seeded;
  }
  var stored = wset3Read(key);
  if (stored && stored.length === n) {
    return stored;
  }
  var order = wset3Identity(n);
  var i;
  for (i = n - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = order[i];
    order[i] = order[j];
    order[j] = tmp;
  }
  return order;
}

function wset3LoadOrder(key, n) {
  var stored = wset3Read(key);
  if (stored && stored.length === n) {
    return stored;
  }
  var seeded = wset3DroidOrder(n);
  if (seeded) {
    return seeded;
  }
  return wset3Identity(n);
}

function wset3Identity(n) {
  var order = [];
  for (var i = 0; i < n; i++) {
    order.push(i);
  }
  return order;
}

function wset3DroidOrder(n) {
  try {
    if (!window.AnkiDroidJS || !AnkiDroidJS.ankiGetCardId || !AnkiDroidJS.ankiGetCardReps) {
      return null;
    }
    return wset3SeededOrder(
      n,
      String(AnkiDroidJS.ankiGetCardId()) + ":" + String(AnkiDroidJS.ankiGetCardReps())
    );
  } catch (e) {
    return null;
  }
}

function wset3SeededOrder(n, seedStr) {
  var x = 1779033703;
  var i;
  for (i = 0; i < seedStr.length; i++) {
    x = Math.imul(x ^ seedStr.charCodeAt(i), 3432918353);
    x = (x << 13) | (x >>> 19);
  }
  x = x >>> 0;
  var order = wset3Identity(n);
  for (i = n - 1; i > 0; i--) {
    x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
    var j = x % (i + 1);
    var tmp = order[i];
    order[i] = order[j];
    order[j] = tmp;
  }
  return order;
}

function wset3SaveOrder(key, order) {
  wset3Write(key, order);
}

function wset3Write(key, value) {
  var raw = JSON.stringify(value);
  try {
    sessionStorage.setItem(key, raw);
  } catch (e) {}
  try {
    localStorage.setItem(key, raw);
  } catch (e) {}
  try {
    window._wset3 = window._wset3 || {};
    window._wset3[key] = value;
  } catch (e) {}
  try {
    var bag = {};
    if (window.name && window.name.indexOf("{") === 0) {
      bag = JSON.parse(window.name);
    }
    bag[key] = value;
    window.name = JSON.stringify(bag);
  } catch (e) {}
}

function wset3Read(key) {
  try {
    if (window._wset3 && window._wset3[key] != null) {
      return window._wset3[key];
    }
  } catch (e) {}
  try {
    if (window.name && window.name.indexOf("{") === 0) {
      var bag = JSON.parse(window.name);
      if (bag[key] != null) {
        return bag[key];
      }
    }
  } catch (e) {}
  var raw = null;
  try {
    raw = sessionStorage.getItem(key);
  } catch (e) {}
  if (!raw) {
    try {
      raw = localStorage.getItem(key);
    } catch (e) {}
  }
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw);
  } catch (e) {
    return null;
  }
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

function wset3PickKey(key) {
  return key + ":pick";
}

function wset3SavePick(key, dataI) {
  wset3Write(wset3PickKey(key), String(dataI));
}

function wset3LoadPick(key) {
  var value = wset3Read(wset3PickKey(key));
  return value == null ? null : String(value);
}

function wset3EnablePicks(box, key) {
  box.classList.add("is-live");
  var nodes = box.querySelectorAll(".choice");
  var i;
  for (i = 0; i < nodes.length; i++) {
    wset3BindTap(nodes[i], function (el) {
      wset3Choose(box, key, el);
    });
  }
}

function wset3BindTap(el, fn) {
  el.setAttribute("role", "button");
  el.setAttribute("tabindex", "0");
  var armed = false;
  function fire(ev) {
    if (armed) {
      return;
    }
    armed = true;
    if (ev) {
      ev.preventDefault();
      ev.stopPropagation();
    }
    fn(el);
    setTimeout(function () {
      armed = false;
    }, 400);
  }
  try {
    el.addEventListener("touchend", fire, { passive: false });
  } catch (e) {
    el.addEventListener("touchend", fire, false);
  }
  el.addEventListener("click", fire, false);
  el.addEventListener(
    "keydown",
    function (ev) {
      if (ev.key === "Enter" || ev.key === " ") {
        fire(ev);
      }
    },
    false
  );
}

function wset3Choose(box, key, el) {
  if (!el || box.getAttribute("data-locked") === "1") {
    return;
  }
  box.setAttribute("data-locked", "1");
  var nodes = box.querySelectorAll(".choice");
  var i;
  for (i = 0; i < nodes.length; i++) {
    nodes[i].classList.remove("selected");
  }
  el.classList.add("selected");
  wset3SavePick(key, el.getAttribute("data-i"));
  wset3ShowAnswer();
}

function wset3MarkPick(box, dataI) {
  if (dataI == null || dataI === "") {
    return;
  }
  var nodes = box.querySelectorAll(".choice");
  var i;
  for (i = 0; i < nodes.length; i++) {
    if (nodes[i].getAttribute("data-i") === String(dataI)) {
      nodes[i].classList.add("picked");
      if (!nodes[i].classList.contains("correct")) {
        nodes[i].classList.add("miss");
      }
    }
  }
}

function wset3ShowAnswer() {
  setTimeout(function () {
    try {
      if (typeof pycmd === "function") {
        pycmd("ans");
        return;
      }
    } catch (e) {}
    try {
      if (typeof showAnswer === "function") {
        showAnswer();
        return;
      }
    } catch (e) {}
    try {
      if (window.AnkiDroidJS && AnkiDroidJS.ankiShowAnswer) {
        AnkiDroidJS.ankiShowAnswer();
        return;
      }
    } catch (e) {}
    try {
      if (typeof window.sendMessage2 === "function") {
        window.sendMessage2("ankitap", "midCenter");
        return;
      }
    } catch (e) {}
    try {
      if (
        window.webkit &&
        window.webkit.messageHandlers &&
        window.webkit.messageHandlers.cb
      ) {
        window.webkit.messageHandlers.cb.postMessage(
          JSON.stringify({ scheme: "ankitap", msg: "midCenter" })
        );
      }
    } catch (e) {}
  }, 80);
}
