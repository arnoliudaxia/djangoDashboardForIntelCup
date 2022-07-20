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

function retriveMeterData(guid,chart,neartime)
{
var meterDataGet;
    $.get(`labdb/retrive?guid=${guid}&nearseconds=${neartime}`,function (response)
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