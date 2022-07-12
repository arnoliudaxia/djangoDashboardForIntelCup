console.log("应用自建文件meterData.js")
function recordData(guid,value)
{
    $.get(`labdb/record?guid=${guid}&value=${value}`,function (response)
    {
        if (response!=="200")
        {
            alert(response);
        }
        retriveMeterData();
    });
}

function retriveMeterData()
{
var meterDataGet;
    $.get("labdb/retrive?guid=11c5ad50-00f6-11ed-a237-087190749d3d",function (response)
    {
        chart.data.datasets[0].label=response.meterName;
       meterDataGet=response.meterData;
        chart.data.labels=[];
       chart.data.datasets.data=[];
       for(let i =0;i<meterDataGet.length;i++)
       {
           chart.data.labels.push(meterDataGet[i].time);
           chart.data.labels[i]=chart.data.labels[i].slice(5);
           chart.data.datasets[0].data.push(meterDataGet[i].value);
       }
       chart.update()
    });
}