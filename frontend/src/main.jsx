import React,{useEffect,useState} from "react";
import {createRoot} from "react-dom/client";
import {LineChart,Line,XAxis,YAxis,CartesianGrid,Tooltip,Legend,ResponsiveContainer} from "recharts";
import "./styles.css";

const API=import.meta.env.VITE_API_URL||"http://localhost:8000";

function App(){
 const [status,setStatus]=useState({history:[]});
 const [health,setHealth]=useState(null);
 async function refresh(){
  try{
   const [s,h]=await Promise.all([
    fetch(API+"/api/status").then(r=>r.json()),
    fetch(API+"/api/health").then(r=>r.json())
   ]);
   setStatus(s);setHealth(h);
  }catch(e){console.error(e)}
 }
 useEffect(()=>{refresh();const id=setInterval(refresh,2000);return()=>clearInterval(id)},[]);
 const s=status.sensor||{},d=status.decision||{};
 const chart=(status.history||[]).slice(0,20).reverse().map((x,i)=>({i,latency:x.processing_latency_ms||0,network:x.network_latency_ms||0}));
 return React.createElement("div",{className:"app"},
  React.createElement("header",null,
   React.createElement("div",null,
    React.createElement("p",{className:"eyebrow"},"RESEARCH PROTOTYPE"),
    React.createElement("h1",null,"IoT Edge Cloud Orchestrator"),
    React.createElement("p",{className:"sub"},"MQTT • Priority Engine • ML Decisioning • Firebase • Edge/Cloud")
   ),
   React.createElement("span",{className:health?.status==="ok"?"pill ok":"pill"},health?.status==="ok"?"ONLINE":"OFFLINE")
  ),
  React.createElement("section",{className:"grid"},
   React.createElement(Card,{title:"Temperature",value:s.temperature!=null?String(s.temperature)+" °C":"—"}),
   React.createElement(Card,{title:"Humidity",value:s.humidity!=null?String(s.humidity)+" %":"—"}),
   React.createElement(Card,{title:"Motion",value:s.motion?"Detected":"Normal"}),
   React.createElement(Card,{title:"Smoke / Intrusion",value:s.smoke||s.intrusion?"Alert":"Normal"}),
   React.createElement(Card,{title:"Decision",value:d.decision||"—",accent:true}),
   React.createElement(Card,{title:"Priority",value:d.priority||"—"}),
   React.createElement(Card,{title:"Latency",value:d.processing_latency_ms!=null?String(d.processing_latency_ms)+" ms":"—"}),
   React.createElement(Card,{title:"Edge CPU",value:d.edge_cpu_percent!=null?String(d.edge_cpu_percent)+"%":"—"})
  ),
  React.createElement("section",{className:"panel"},
   React.createElement("div",{className:"panelHead"},React.createElement("h2",null,"Latency"),React.createElement("span",null,String(chart.length)+" recent decisions")),
   React.createElement("div",{className:"chart"},
    React.createElement(ResponsiveContainer,{width:"100%",height:"100%"},
     React.createElement(LineChart,{data:chart},
      React.createElement(CartesianGrid,{strokeDasharray:"3 3"}),
      React.createElement(XAxis,{dataKey:"i"}),
      React.createElement(YAxis,null),
      React.createElement(Tooltip,null),
      React.createElement(Legend,null),
      React.createElement(Line,{type:"monotone",dataKey:"latency",strokeWidth:3,name:"Processing ms"}),
      React.createElement(Line,{type:"monotone",dataKey:"network",strokeWidth:2,name:"Network ms"})
     )
    )
   )
  ),
  React.createElement("section",{className:"panel"},
   React.createElement("div",{className:"panelHead"},React.createElement("h2",null,"Recent Decisions"),React.createElement("span",null,String((status.history||[]).length)+" tracked")),
   React.createElement("div",{className:"table"},
    React.createElement("div",{className:"row head"},["Task","Priority","Decision","Latency","Source"].map(x=>React.createElement("span",{key:x},x))),
    (status.history||[]).slice(0,10).map((x,i)=>React.createElement("div",{className:"row",key:i},
     React.createElement("span",null,x.task_type||"—"),
     React.createElement("span",null,x.priority||"—"),
     React.createElement("span",{className:x.decision==="EDGE"?"tag edge":"tag cloud"},x.decision),
     React.createElement("span",null,String(x.processing_latency_ms||0)+" ms"),
     React.createElement("span",null,x.decision_source||"—")
    ))
   )
  )
 );
}

function Card({title,value,accent}){return React.createElement("div",{className:"card "+(accent?"accent":"")},React.createElement("span",null,title),React.createElement("strong",null,value))}
createRoot(document.getElementById("root")).render(React.createElement(App));