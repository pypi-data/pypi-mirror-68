$(document).ready(function () {
  var menu = document.querySelector(".hamburger-menu");
  var bar = document.querySelector(".nav-bar");
  menu.addEventListener("click", () => {
    bar.classList.toggle("change");
  });
  $("select").niceSelect();
  GetDataState();
  $("#daily").change(function () {
    var el = $(this);
    // console.log(el.val());
    if (el.val() === "Yes" && $("#state_name").val() === "All") {
      console.log(el.val());
      var children = document.getElementById("Daily_bar").children;
      id = children[children.length - 2].getAttribute("id");
      if (id != "daily_1") {
        $("#Daily_bar").append(
          "<select id='daily_1'><option value='Confirmed'>Confirmed</option><option value='Recovered'>Recovered</option><option value='Death'>Death</option></select>"
        );
        $("select").niceSelect();
      }
    } else if ($("#state_name").val() != "All" && el.val() === "Yes") {
      var children = document.getElementById("Daily_bar").children;
      id = children[children.length - 2].getAttribute("id");
      if (id === "daily_1") {
        $("#daily_1").remove();
        $("#Daily_bar div:last-child").remove();
      }
    } else if ($("#state_name").val() === "All" && el.val() === "No") {
      var children = document.getElementById("Daily_bar").children;
      id = children[children.length - 2].getAttribute("id");
      if (id === "daily_1") {
        $("#daily_1").remove();
        $("#Daily_bar div:last-child").remove();
      }
    }
    GetDataState();
  });
  $("#state_name").change(function () {
    var et = $(this);
    // console.log(et.val());
    if (et.val() === "All" && $("#daily").val() === "Yes") {
      var children = document.getElementById("Daily_bar").children;
      id = children[children.length - 2].getAttribute("id");
      if (id != "daily_1") {
        $("#Daily_bar").append(
          "<select id='daily_1'><option value='Confirmed'>Confirmed</option><option value='Recovered'>Recovered</option><option value='Death'>Death</option></select>"
        );
        $("select").niceSelect();
      }
    } else if (et.val() != "All" && $("#daily").val() === "Yes") {
      var children = document.getElementById("Daily_bar").children;
      id = children[children.length - 2].getAttribute("id");
      if (id === "daily_1") {
        $("#daily_1").remove();
        $("#Daily_bar div:last-child").remove();
      }
    }
    GetDataState();
  });

  $(document.body).on("change", "#daily_1", function () {
    var et = $(this);
    console.log(et.val());
    GetDataState();
  });
});
// console.log(et);
// console.log(el);

//  else {
//   $("#Daily_bar select:last-child").remove();
// }
// var chil = document.getElementById("Daily_bar").children[1];
// console.log(chil.getAttribute("id"));

function GetDataState() {
  var e = document.getElementById("state_name");
  var state_name = e.options[e.selectedIndex].text;

  var p = document.getElementById("daily");
  var daily = p.options[p.selectedIndex].text;

  var q = document.getElementById("daily_1");

  if (q != null) {
    console.log(q.options[q.selectedIndex].text);
    var condition = q.options[q.selectedIndex].text;
  }
  $.post(
    "/State",
    {
      state_data: JSON.stringify(state_name),
      daily_data: JSON.stringify(daily),
      condition_data: JSON.stringify(condition),
    },
    function (data, status, xhr) {
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
      console.log(JSON.parse(data));
      console.log(Object.keys(df[0]));
      divShowData.innerHTML = "";
      divShowData.appendChild(table);
      divShowData.style.width = "auto";
      divShowData.style.maxWidth = "900px";
      divShowData.style.maxHeight = "500px";
      // divShowData.style.background = "grey";
      divShowData.style.overflow = "auto";
      divShowData.style.marginTop = "20px";
      // divShowData.style.marginLeft = "50%";
    }
  );
}
