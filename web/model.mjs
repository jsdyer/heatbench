export const FACTORS=Object.freeze({oil:10.61,gas:10.36,propane:7.03,electric:1,delivered:1});
export function number(value,name,min=0,max=1e9){if(value===''||value==null)throw new Error(`Enter ${name}.`);const n=Number(value);if(!Number.isFinite(n)||n<min||n>max)throw new Error(`${name} must be between ${min} and ${max}.`);return n;}
export function calculate(s){
 if(!(s.fuel in FACTORS))throw new Error('Choose a supported heating fuel.');
 const units=number(s.annualUnits,'annual energy use',0,1e7),fraction=number(s.spaceHeatPercent,'space-heating share',0,100)/100;
 const efficiency=s.fuel==='electric'||s.fuel==='delivered'?1:number(s.efficiency,'existing efficiency',1,100)/100;
 const factor=number(s.weatherFactor,'weather adjustment',.1,3),heat=units*FACTORS[s.fuel]*fraction*efficiency*factor;
 const fuel=number(s.fuelPrice,'fuel price',0,100),electric=number(s.electricPrice,'electricity price',0,10);
 const copLow=number(s.copLow,'lower seasonal COP',.5,8),copHigh=number(s.copHigh,'higher seasonal COP',.5,8);
 if(copLow>copHigh)throw new Error('Lower COP must not exceed higher COP.');
 const backup=number(s.backupPercent,'backup heat share',0,100)/100;
 if(!['electric','existing'].includes(s.backup))throw new Error('Choose a supported backup system.');
 const baseline=s.fuel==='delivered'?heat*fuel:heat/(FACTORS[s.fuel]*efficiency)*fuel;
 const maintenance=number(s.maintenanceDifference,'additional annual maintenance',-10000,10000);
 const backupCost=backup*(s.backup==='existing'?baseline:heat*electric);
 const pump=(cop)=>heat*(1-backup)/cop*electric+backupCost+maintenance;
 const highCost=pump(copLow),lowCost=pump(copHigh),savingsLow=baseline-highCost,savingsHigh=baseline-lowCost;
 const installation=number(s.installationCost,'net installation cost',0,1e6);
 return {heat,baseline,resistance:heat*electric,lowCost,highCost,savingsLow,savingsHigh,paybackLow:savingsHigh>0?installation/savingsHigh:null,paybackHigh:savingsLow>0?installation/savingsLow:null,copLow,copHigh};
}
export function csv(s,r){return 'field,value\n'+Object.entries({...s,...r}).map(([k,v])=>[k,v==null?'not reached':v].map(x=>'"'+String(x).replaceAll('"','""')+'"').join(',')).join('\n');}
