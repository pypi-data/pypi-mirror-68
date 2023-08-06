// var e = document.getElementById("sheet-content");

// // var result = e.options[e.selectedIndex].text;

// console.log(e);
$(document).ready(function () {
  $(".download").on("click", function () {
    var down = document.querySelector(".popDownload");
    down.classList.add("clicked");
    down.classList.toggle("popAfter");
    if (down.classList.contains("clicked")) {
      var appear = document.querySelectorAll(".afterClick");
      appear[0].classList.remove("id1");
      appear[1].classList.remove("id2");
      appear[2].classList.remove("id3");
      var down = document.querySelector(".beforeClick");
      down.style.display = "flex";
    }
  });
  $(".confirm").on("click", function () {
    var down = document.querySelector(".beforeClick");
    down.style.display = "none";
    var appear = document.querySelector(".id-1");
    appear.classList.toggle("id1");
    // appear.style.display = "block";
    appear.style.background = "antiquewhite";
  });
  $(".Recover").on("click", function () {
    var down = document.querySelector(".beforeClick");
    down.style.display = "none";
    var appear = document.querySelector(".id-2");
    appear.classList.toggle("id2");
    // appear.style.display = "block";
    appear.style.background = "antiquewhite";
  });
  $(".Death").on("click", function () {
    var down = document.querySelector(".beforeClick");
    down.style.display = "none";
    var appear = document.querySelector(".id-3");
    appear.classList.toggle("id3");
    // appear.style.display = "block";
    appear.style.background = "antiquewhite";
  });
  $(".cross").on("click", function () {
    var appear = document.querySelectorAll(".afterClick");
    // console.log(appear[0]);
    appear[0].classList.remove("id1");
    appear[1].classList.remove("id2");
    appear[2].classList.remove("id3");
    var down = document.querySelector(".beforeClick");
    down.style.display = "flex";
  });
  $(".cross-1").on("click", function () {
    var appear = document.querySelector(".popDownload");
    // console.log(appear[0]);
    appear.classList.remove("popAfter");
  });
  // document.onclick = function (e) {
  //   if (e.target.id !== "divToHide") {
  //     //element clicked wasn't the div; hide the div
  //     var appear = document.querySelectorAll(".afterClick");
  //     appear[0].classList.remove("id1");
  //     appear[1].classList.remove("id2");
  //     appear[2].classList.remove("id3");
  //     var down = document.querySelector(".beforeClick");
  //     down.style.display = "flex";
  //     divToHide.style.display = "none";
  //   }
  // };
  // $("li:eq(0)").addClass("active");
  var menu = document.querySelector(".hamburger-menu");
  var bar = document.querySelector(".nav-bar");
  menu.addEventListener("click", () => {
    bar.classList.toggle("change");
  });
  $("select").niceSelect();
  $(".nice-select").css({
    height: "25px",
    "text-align": "center",
    background: "transparent",
    border: "none",
    "border-bottom": "1px solid red",
    "border-radius": "2px",
    width: "300px",
    display: "inline-block",
    left: "42%",
    top: "-5px",
  });
  $(".current").css({
    position: "relative",
    top: "-5px",
    right: "-16px",
    color: "white",
    "font-size": "17px",
    width: "100px",
    "text-align": "center",
  });
  $(".list").css({
    width: "300px",
    "font-size": "17px",
    background: "rgb(106, 86, 81 )",
    color: "rgb(237, 236, 235)",
  });

  GetSelectedText();
  var list = ["Total Confirmed"];
  function onchange() {
    var spanText = $(".current").text();
    if (list.includes(spanText) == false) {
      list = [];
      list.push(spanText);
      GetSelectedText();
    }
  }
  setInterval(onchange, 10);
});

function GetSelectedText() {
  // var e = document.getElementsByClassName("current");
  var result = $(".current").text();
  $.post(
    "/data",
    {
      result_data: result,
    },
    function (data, status, xhr) {
      console.log(data);
      var df = JSON.parse(data);
      // Extract value from table header.
      var col = [];
      for (var i = 0; i < df.length; i++) {
        for (var key in df[i]) {
          if (col.indexOf(key) === -1) {
            col.push(key);
          }
        }
      }

      // Create a table.
      var table = document.createElement("table");

      // Create table header row using the extracted headers above.
      var tr = table.insertRow(-1); // table row.

      for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th"); // table header.
        th.innerHTML = col[i];
        tr.appendChild(th);
      }

      // add json data to the table as rows.
      for (var i = 0; i < df.length; i++) {
        tr = table.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
          var tabCell = tr.insertCell(-1);
          tabCell.innerHTML = df[i][col[j]];
        }
      }
      var divShowData = document.getElementById("data_show");
      // console.log(JSON.parse(data));
      // console.log(Object.values(df[0]));
      divShowData.innerHTML = "";
      divShowData.appendChild(table);
      divShowData.style.width = "auto";
      divShowData.style.maxWidth = "150vh";
      divShowData.style.height = "90vh";
      // divShowData.style.background = "grey";
      divShowData.style.overflow = "auto";
      divShowData.style.marginTop = "20px";
    }
  );

  //   console.log(result);
  // document.getElementById("result").innerHTML = result;
}
