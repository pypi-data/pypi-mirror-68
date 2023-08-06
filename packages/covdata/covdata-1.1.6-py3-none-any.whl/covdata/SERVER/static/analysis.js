$(document).ready(function () {
  var slider_1 = document.getElementById("slider-1");
  var silder_value_1 = document.getElementById("value-1");

  var menu = document.querySelector(".hamburger-menu");
  var bar = document.querySelector(".nav-bar");

  slider_1.oninput = function () {
    silder_value_1.innerHTML = this.value;
  };

  menu.addEventListener("click", () => {
    bar.classList.toggle("change");
  });
  $("select").niceSelect();
  var state = $("#graph-state").val();
  var Daily = $("#daily").val();
  var cond = $("#cond-id").val();
  var slide = $("#slider-1").val();
  if (Daily === "Yes") {
    var q = "Daily";
  } else {
    var q = "cumulative";
  }
  $.post(
    "/analysis",
    {
      state_data: JSON.stringify(state),
      daily_data: JSON.stringify(Daily),
      condition_data: JSON.stringify(cond),
      silder_data: slide,
    },
    function (data, status, xhr) {
      // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
      if (cond != "Together") {
        var response = {
          labels: Object.keys(data[0]).slice(1),
          datasets: [
            {
              label: state + " " + q + " Count cases " + cond,
              data: Object.values(data[data.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: ["rgba(255, 0, 0, 1)"],
              fill: false,
              borderWidth: 1,
            },
          ],
        };
        var ctx = document.getElementById("graph").getContext("2d");
        GetGraphData("line", response, ctx, (id = 1));
      } else {
        var cond_list = ["Confirmed", "Recovered", "Deceased"];
        var border_Color = [
          "rgba(255, 0, 0, 1)",
          "rgba(0, 255, 0, 1)",
          "rgba(0, 0, 255, 1)",
        ];
        var d = [];
        for (i = 0; i < data.length; i++) {
          var df = JSON.parse(data[i]);
          d.push({
            label: state + " " + q + " Count cases " + cond_list[i],
            data: Object.values(df[df.length - 1]).slice(1),
            backgroundColor: ["rgba(255, 50, 50, 1)"],
            borderColor: border_Color[i],
            fill: false,
            borderWidth: 1,
          });
        }
        var response = {
          labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
          datasets: d,
        };
        var ctx = document.getElementById("graph").getContext("2d");
        GetGraphData("line", response, ctx, (id = 1));
      }
    }
  );
  $("#graph-state").change(function () {
    var state = $(this).val();
    var Daily = $("#daily").val();
    var cond = $("#cond-id").val();
    var slide = $("#slider-1").val();
    if (Daily === "Yes") {
      var q = "Daily";
    } else {
      var q = "cumulative";
    }
    $.post(
      "/analysis",
      {
        state_data: JSON.stringify(state),
        daily_data: JSON.stringify(Daily),
        condition_data: JSON.stringify(cond),
        silder_data: slide,
      },
      function (data, status, xhr) {
        // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
        if (cond != "Together") {
          var response = {
            labels: Object.keys(data[0]).slice(1),
            datasets: [
              {
                label: state + " " + q + " Count cases " + cond,
                data: Object.values(data[data.length - 1]).slice(1),
                backgroundColor: ["rgba(255, 50, 50, 1)"],
                borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        } else {
          var cond_list = ["Confirmed", "Recovered", "Deceased"];
          var border_Color = [
            "rgba(255, 0, 0, 1)",
            "rgba(0, 255, 0, 1)",
            "rgba(0, 0, 255, 1)",
          ];
          var d = [];
          for (i = 0; i < data.length; i++) {
            var df = JSON.parse(data[i]);
            d.push({
              label: state + " " + q + " Count cases " + cond_list[i],
              data: Object.values(df[df.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: border_Color[i],
              fill: false,
              borderWidth: 1,
            });
          }
          var response = {
            labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
            datasets: d,
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        }
      }
    );
  });
  $("#daily").change(function () {
    var state = $("#graph-state").val();
    var Daily = $(this).val();
    var cond = $("#cond-id").val();
    var slide = $("#slider-1").val();
    if (Daily === "Yes") {
      var q = "Daily";
    } else {
      var q = "cumulative";
    }
    $.post(
      "/analysis",
      {
        state_data: JSON.stringify(state),
        daily_data: JSON.stringify(Daily),
        condition_data: JSON.stringify(cond),
        silder_data: slide,
      },
      function (data, status, xhr) {
        // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
        if (cond != "Together") {
          var response = {
            labels: Object.keys(data[0]).slice(1),
            datasets: [
              {
                label: state + " " + q + " Count cases " + cond,
                data: Object.values(data[data.length - 1]).slice(1),
                backgroundColor: ["rgba(255, 50, 50, 1)"],
                borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        } else {
          var cond_list = ["Confirmed", "Recovered", "Deceased"];
          var border_Color = [
            "rgba(255, 0, 0, 1)",
            "rgba(0, 255, 0, 1)",
            "rgba(0, 0, 255, 1)",
          ];
          var d = [];
          for (i = 0; i < data.length; i++) {
            var df = JSON.parse(data[i]);
            d.push({
              label: state + " " + q + " Count cases " + cond_list[i],
              data: Object.values(df[df.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: border_Color[i],
              fill: false,
              borderWidth: 1,
            });
          }
          var response = {
            labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
            datasets: d,
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        }
      }
    );
  });
  $("#cond-id").change(function () {
    var state = $("#graph-state").val();
    var Daily = $("#daily").val();
    var cond = $(this).val();
    var slide = $("#slider-1").val();
    // console.log(cond);
    if (Daily === "Yes") {
      var q = "Daily";
    } else {
      var q = "cumulative";
    }
    $.post(
      "/analysis",
      {
        state_data: JSON.stringify(state),
        daily_data: JSON.stringify(Daily),
        condition_data: JSON.stringify(cond),
        silder_data: slide,
      },
      function (data, status, xhr) {
        // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
        if (cond != "Together") {
          var response = {
            labels: Object.keys(data[0]).slice(1),
            datasets: [
              {
                label: state + " " + q + " Count cases " + cond,
                data: Object.values(data[data.length - 1]).slice(1),
                backgroundColor: ["rgba(255, 50, 50, 1)"],
                borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        } else {
          var cond_list = ["Confirmed", "Recovered", "Deceased"];
          var border_Color = [
            "rgba(255, 0, 0, 1)",
            "rgba(0, 255, 0, 1)",
            "rgba(0, 0, 255, 1)",
          ];
          var d = [];
          for (i = 0; i < data.length; i++) {
            var df = JSON.parse(data[i]);
            d.push({
              label: state + " " + q + " Count cases " + cond_list[i],
              data: Object.values(df[df.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: border_Color[i],
              fill: false,
              borderWidth: 1,
            });
          }
          var response = {
            labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
            datasets: d,
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        }
      }
    );
  });
  $("#slider-1").change(function () {
    var state = $("#graph-state").val();
    var Daily = $("#daily").val();
    var cond = $("#cond-id").val();
    var slide = $(this).val();
    // console.log(cond);
    if (Daily === "Yes") {
      var q = "Daily";
    } else {
      var q = "cumulative";
    }
    $.post(
      "/analysis",
      {
        state_data: JSON.stringify(state),
        daily_data: JSON.stringify(Daily),
        condition_data: JSON.stringify(cond),
        silder_data: slide,
      },
      function (data, status, xhr) {
        // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
        if (cond != "Together") {
          var response = {
            labels: Object.keys(data[0]).slice(1),
            datasets: [
              {
                label: state + " " + q + " Count cases " + cond,
                data: Object.values(data[data.length - 1]).slice(1),
                backgroundColor: ["rgba(255, 50, 50, 1)"],
                borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        } else {
          var cond_list = ["Confirmed", "Recovered", "Deceased"];
          var border_Color = [
            "rgba(255, 0, 0, 1)",
            "rgba(0, 255, 0, 1)",
            "rgba(0, 0, 255, 1)",
          ];
          var d = [];
          for (i = 0; i < data.length; i++) {
            var df = JSON.parse(data[i]);
            d.push({
              label: state + " " + q + " Count cases " + cond_list[i],
              data: Object.values(df[df.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: border_Color[i],
              fill: false,
              borderWidth: 1,
            });
          }
          var response = {
            labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
            datasets: d,
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        }
      }
    );
  });
  // $(window).scroll(function () {
  //   var chart = document.querySelectorAll(".g");

  //   var scrrenPosition = window.innerHeight;
  //   // var positionTop = $(document).scrollTop();

  //   for (i = 0; i < chart.length; i++) {
  //     console.log(chart[i]);
  //     var chart2Position = chart[i].getBoundingClientRect().top;
  //     console.log(chart2Position);
  //     console.log(scrrenPosition);
  //     if (chart2Position < scrrenPosition / 1.2) {
  //       console.log("yes");
  //       $(".g").removeClass("animated bounceOutLeft");
  //       $(".g").addClass("animated bounceInLeft");
  //     } else {
  //       $(".g").removeClass("animated bounceInLeft");
  //       $(".g").addClass("animated bounceOutLeft");
  //     }
  //   }
  // });
  if ($("#g-2_chk-2").is(":checked")) {
    $.post(
      "/tested",
      {
        ratio_data: "true",
      },
      function (data, status, xhr) {
        var xlabel = [];
        var ylabel = [];
        var color = [];
        var op = 1;
        for (i = 0; i < data.length; i++) {
          xlabel.push(Object.values(data[i])[0]);
          ylabel.push(Object.values(data[i])[4]);
          color.push("rgba(0,255,0," + op + ")");
          op = op - 1 / (data.length + 5);
        }

        var response = {
          labels: xlabel,
          datasets: [
            {
              label: "Confirmed to Test Ratio(F)",
              data: ylabel,
              backgroundColor: color,
              // borderColor: ["rgba(255, 0, 0, 1)"],
              fill: false,
              borderWidth: 1,
            },
          ],
        };
        var ctx = document.getElementById("graph-2").getContext("2d");
        GetGraphData("bar", response, ctx, (id = 2));
      }
    );
  }
  $("#g-2_chk-2").change(function () {
    if ($("#g-2_chk-2").is(":checked")) {
      $.post(
        "/tested",
        {
          ratio_data: "true",
        },
        function (data, status, xhr) {
          var xlabel = [];
          var ylabel = [];
          var color = [];
          var op = 1;
          for (i = 0; i < data.length; i++) {
            xlabel.push(Object.values(data[i])[0]);
            ylabel.push(Object.values(data[i])[4]);
            color.push("rgba(0,255,0," + op + ")");
            op = op - 1 / (data.length + 5);
          }

          var response = {
            labels: xlabel,
            datasets: [
              {
                label: "Confirmed to Test Ratio(F)",
                data: ylabel,
                backgroundColor: color,
                // borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph-2").getContext("2d");
          GetGraphData("bar", response, ctx, (id = 2));
        }
      );
    }
  });
  $("#g-2_chk-1").change(function () {
    if ($("#g-2_chk-1").is(":checked")) {
      {
        $.post(
          "/tested",
          {
            ratio_data: "false",
          },
          function (data, status, xhr) {
            console.log(data);
            var xlabel = [];
            var ylabel = [];
            var color = [];
            var op = 1;
            for (i = 0; i < data.length; i++) {
              xlabel.push(Object.values(data[i])[0]);
              ylabel.push(Object.values(data[i])[6]);
              color.push("rgba(0,255,0," + op + ")");
              op = op - 1 / (data.length + 5);
            }
            var response = {
              labels: xlabel,
              datasets: [
                {
                  label: "Total tested",
                  data: ylabel,
                  backgroundColor: color,
                  // borderColor: ["rgba(255, 0, 0, 1)"],
                  fill: false,
                  borderWidth: 1,
                },
              ],
            };
            var ctx = document.getElementById("graph-2").getContext("2d");
            GetGraphData("bar", response, ctx, (id = 2));
          }
        );
      }
    }
  });
  $.post(
    "/rec_dec_rate",
    {
      rate: "recovered",
    },
    function (data, status, xhr) {
      console.log(data);
      var xlabel = [];
      var ylabel = [];
      var color = [];
      var border = [];
      var op = 0.83;
      for (i = 0; i < data.length; i++) {
        xlabel.push(Object.values(data[i])[0]);
        ylabel.push(Object.values(data[i])[4]);
        color.push("rgba(174,255,215," + op + ")");
        border.push("rgba(174,255,215,0.91)");
        op = op - 1 / (data.length + 5);
      }
      var response = {
        labels: xlabel,
        datasets: [
          {
            label: "Recovery Rate(R)",
            data: ylabel,
            backgroundColor: color,
            barThickness: 15,
            borderColor: border,
            fill: false,
            borderWidth: 1,
          },
        ],
      };
      var ctx = document.getElementById("graph-3").getContext("2d");
      GetGraphData("horizontalBar", response, ctx, (id = 3));
    }
  );
  $.post(
    "/rec_dec_rate",
    {
      rate: "deceased",
    },
    function (data, status, xhr) {
      console.log(data);
      var xlabel = [];
      var ylabel = [];
      var color = [];
      var border = [];
      var op = 0.83;
      for (i = 0; i < data.length; i++) {
        xlabel.push(Object.values(data[i])[0]);
        ylabel.push(Object.values(data[i])[5]);
        color.push("rgba(131,247,244," + op + ")");
        border.push("rgba(131,247,244,0.91)");
        op = op - 1 / (data.length + 5);
      }
      var response = {
        labels: xlabel,
        datasets: [
          {
            label: "Deceased Rate(D)",
            data: ylabel,
            backgroundColor: color,
            barThickness: 15,
            borderColor: border,
            fill: false,
            borderWidth: 1,
          },
        ],
      };
      var ctx = document.getElementById("graph-4").getContext("2d");
      GetGraphData("horizontalBar", response, ctx, (id = 4));
    }
  );
});
function GetGraphData(e, f, g, id) {
  if (id == 1) {
    if (window.myChart) window.myChart.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart = new Chart(g, {
      type: e,
      data: f,
      options: {
        animation: {
          duration: 2000,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "rgba(255, 255, 255,0.5)",
              },
            },
          ],
          xAxes: [
            {
              ticks: {
                fontColor: "rgba(255, 255, 255,0.5)",
              },
            },
          ],
        },
        tooltips: {
          mode: "x",
        },
        legend: {
          display: true,
          labels: {
            fontColor: "rgba(255, 255, 255,0.8)",
          },
        },
      },
    });
  }
  if (id == 2) {
    if (window.myChart2) window.myChart2.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart2 = new Chart(g, {
      type: e,
      data: f,
      options: {
        animation: {
          duration: 2000,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "rgba(255, 255, 255,0.5)",
              },
            },
          ],
          xAxes: [
            {
              ticks: {
                fontColor: "rgba(255, 255, 255,0.5)",
              },
            },
          ],
        },
        tooltips: {
          mode: "x",
        },
        legend: {
          display: true,
          labels: {
            fontColor: "rgba(255, 255, 255,0.8)",
          },
        },
      },
    });
  }
  if (id == 3) {
    if (window.myChart3) window.myChart3.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart3 = new Chart(g, {
      type: e,
      data: f,
      options: {
        animation: {
          duration: 2000,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "rgba(255, 255, 255,0.5)",
              },
            },
          ],
          xAxes: [
            {
              categoryPercentage: 1.0,
              barPercentage: 0.5,
              ticks: {
                fontColor: "rgba(255, 255, 255,0.5)",
              },
            },
          ],
        },
        tooltips: {
          mode: "index",
        },
        legend: {
          display: true,
          labels: {
            fontColor: "rgba(255, 255, 255,0.8)",
          },
        },
      },
    });
  }
  if (id == 4) {
    if (window.myChart4) window.myChart4.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart4 = new Chart(g, {
      type: e,
      data: f,
      options: {
        animation: {
          duration: 2000,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "rgba(255, 255, 255,0.5)",
              },
            },
          ],
          xAxes: [
            {
              categoryPercentage: 1.0,
              barPercentage: 0.5,
              ticks: {
                fontColor: "rgba(255, 255, 255,0.5)",
              },
            },
          ],
        },
        tooltips: {
          mode: "index",
        },
        legend: {
          display: true,
          labels: {
            fontColor: "rgba(255, 255, 255,0.8)",
          },
        },
      },
    });
  }
}
