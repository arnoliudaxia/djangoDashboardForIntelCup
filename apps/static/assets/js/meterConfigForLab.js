<!--AJAX加载仪表配置-->
function flashMeterTable() {
    var Showtable = document.getElementById("meterConfigTable")
    var tableHead = Showtable.children[0].children[0];
    var tableBody = Showtable.children[1];
    // clear table content
    tableHead.innerHTML = "";
    tableBody.innerHTML = "";
    var meterconfigs;
    $.get("labdb/meterconfig", function (data) {
        // console.log(data);
        meterconfigs = data;
        //添加表头，也是数据库里的所有字段
        let labels = meterconfigs.labels;

        for (let i = 0; i < labels.length; i++) {
            console.log(labels[i]);
            let newth = document.createElement("th");
            newth.innerText = labels[i];
            tableHead.appendChild(newth);
        }
        //现在开始整表体
        let meters = meterconfigs.meters;
        for (let i = 0; i < meters.length; i++) {
            console.log(meters[i]);
            let newrow = document.createElement("tr");
            for (var key in meters[i]) {
                let newth = document.createElement("th");
                newth.innerText = meters[i][key];
                newrow.appendChild(newth);

            }

            tableBody.appendChild(newrow);
        }

    });
}


$(function () {
    flashMeterTable();
});

function registerMeter(thisbtn) {
    thisbtn.innerText = "注册中";
    let meterName = document.getElementById("meterName").value;
    if (meterName === '') {
        alert("请输入表名!");
        return;
    }
    $.get("labdb/register?name=" + meterName, function (response) {
        {
            alert(response);

        }

        flashMeterTable();
        thisbtn.innerText = "注册仪表";
    })
}

function removeMeter(thisbtn) {
    thisbtn.innerText = "删除中";

    let meterGUID = document.getElementById("meterGUID2Remove").value;
    if (meterGUID === '') {
        alert("请输入表的GUID！可以从上方的表格中复制");
        return;
    }
    $.get("labdb/remove?guid=" + meterGUID, function (response) {
        if (response !== "200") {
            alert(response);

        }
        flashMeterTable();
        thisbtn.innerText = "删除仪表";

    })

}