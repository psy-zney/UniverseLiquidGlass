return (async()=>{
  const w=Services.wm.getMostRecentWindow('navigator:browser'),d=w.document;
  const {Downloads}=ChromeUtils.importESModule('resource://gre/modules/Downloads.sys.mjs');
  const list=await Downloads.getList(Downloads.ALL);
  if(!w.__cosmosDownloads && !(await list.getAll()).length) {
    w.__cosmosDownloads=true;
    const entries=[
      ['UniverseLiquidGlass-v1.0.0.zip', 'https://example.test/theme', 337_000],
      ['The universe — a guide to stars, galaxies and black holes.pdf', 'https://example.test/guide', 8_450_000],
      ['UniverseLiquidGlass-native-Zen-demo.mp4', 'https://example.test/demo', 4_280_000],
      ['Moved-space-wallpaper.jpg','https://example.test/image',580_000],
    ];
    for(let i=0;i<entries.length;i++) {
      const [name,url,bytes]=entries[i];
      const target=PathUtils.join(Services.dirsvc.get('ProfD',Ci.nsIFile).path,name);
      if(i!==3) await IOUtils.writeUTF8(target,'Theme preview sample.');
      const dl=await Downloads.createDownload({source:{url},target:{path:target}});
      dl.succeeded=true;dl.stopped=true;dl.hasProgress=true;dl.totalBytes=bytes;dl.currentBytes=bytes;
      dl.startTime=new Date();dl.endTime=new Date();
      await list.add(dl);
    }
  }
  return {opened:true,count:(await list.getAll()).length};
})();
