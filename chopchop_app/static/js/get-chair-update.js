$(document).ready(function () {

    alert("Welcome! \nWe also glad that you check out our prototype. \nPlease contact CHOP CHOPE team to set up the seat sensors." +
        "\n \n" +
        "The demo only works on iPad Pro landscape mode or a wider screen.");


    getUpdates();

    // remove comment below causes the sendRequest function to run every 5 seconds
    window.setInterval(getUpdates, 5000);


});


function getUpdates() {

    $.ajax({
        'url': '/get-chair-status',
        'type': 'GET',
        'data': "text",
        'dataType': "text",
        success: onGetUpdates,
        error: function (data) {
            console.log("fail" + data);
        }
    });

    function onGetUpdates(data) {

        //console.log("update post : " + data);
        var data = JSON.parse(data.replace(/'/g, "\""));
        //var list = document.getElementById("posts_block");


        chairs = data["chair"];

        if (chairs.length >= 1) {

            // Adds each new chair
            for (var i = 0; i < chairs.length; ++i) {
                // Extracts the chair data
                var chair_code = chairs[i]["chair_code"];  // pk is "primary key", the id
                var chair_status = chairs[i]["status"];
                var in_time = chairs[i]["in_time"];
                var duration = chairs[i]["duration"];

                var pre_duration = (45 - duration).toFixed(2);

                if (isNaN(pre_duration)) {
                    pre_duration = 0;
                }
                else if (pre_duration < 0) {
                    pre_duration = 0;
                }

                if (parseInt(duration) >= 60) {
                    duration = '60+';
                }

                //console.log("chair - " + chair_code +" " +chair_status + " " + in_time + " " + duration);

                if (chair_status == "sit") {
                    var chair_div = '#' + chair_code;
                    var popup_div = $('#popup_html_block').html()
                        .replace(/{x}/g, chair_code)
                        .replace(/{in_time}/g, in_time)
                        .replace(/{duration}/g, duration)
                        .replace(/{predic_duration}/g, pre_duration);

                    var human_div = $('#human_html_block').html();

                    $(chair_div).empty();

                    $(chair_div).append(popup_div);
                    $(chair_div).append(human_div);
                }
                if (chair_status == "free") {
                    var chair_div = '#' + chair_code;

                    $(chair_div).empty();
                }
            }

        } else {
            console.log("no update");
        }

        dashboard_data = data["dashboard"];

        if (dashboard_data.length >= 1) {
            var now_ = dashboard_data[0]["now"];
            var total_person = dashboard_data[0]["total_person"];
            var avg_time = dashboard_data[0]["avg_time"];
            var max_time = dashboard_data[0]["max_time"];
            var min_time = dashboard_data[0]["min_time"];
            var most_pop = dashboard_data[0]["most_pop"];
            var min_pop = dashboard_data[0]["min_pop"];

            var top_bar_in = document.getElementById("dashboard_bar").innerHTML;
            var temp = top_bar_in.replace(/{now_}/g, now_)
                .replace(/{avg_time}/g, avg_time)
                .replace(/{total_person}/g, total_person)
                .replace(/{max_time}/g, max_time)
                .replace(/{min_time}/g, min_time)
                .replace(/{most_pop}/g, most_pop)
                .replace(/{min_pop}/g, min_pop)
            ;
            document.getElementById("dashboard_bar").innerHTML = temp;

        }


    }

}