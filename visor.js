(function(){
  var secs=[].slice.call(document.querySelectorAll('.degrau'));
  var N=secs.length;
  // a trilha: o que o "o" já virou em cada degrau
  var est=__TRILHA__;
  var trilha=document.getElementById('trilha');
  var ant=document.getElementById('ant'),prox=document.getElementById('prox'),pos=document.getElementById('pos');
  var atual=0;
  function desenharTrilha(k){
    var h='';
    for(var i=0;i<est.length;i++){
      var cls=i<k?'passado':(i===k?'atual':'futuro');
      h+='<div class="est '+cls+'" data-i="'+i+'">'+est[i].tok+'<span class="nome">'+est[i].nome+'</span></div>';
    }
    trilha.innerHTML=h;
    var a=trilha.querySelector('.atual'); if(a&&a.scrollIntoView){try{a.scrollIntoView({block:'nearest',inline:'center'});}catch(e){}}
  }
  function ir(k,foco){
    if(k<0||k>=N)return;
    atual=k;
    secs.forEach(function(s,i){s.hidden=(i!==k);});
    desenharTrilha(k);
    var ultimo=(k===N-1);
    pos.textContent= ultimo?'fecho':'degrau '+(k+1)+' de '+(N-1);
    ant.disabled=(k===0); ant.querySelector('span').textContent=k>0?secs[k-1].dataset.nome:'';
    prox.disabled=ultimo; prox.querySelector('span').textContent=!ultimo?secs[k+1].dataset.nome:'';
    try{location.hash=secs[k].id;}catch(e){}
    try{localStorage.setItem('om-degrau',String(k));}catch(e){}
    if(foco){window.scrollTo({top:0,behavior:'auto'});}
  }
  ant.addEventListener('click',function(){ir(atual-1,true);});
  prox.addEventListener('click',function(){ir(atual+1,true);});
  trilha.addEventListener('click',function(e){var t=e.target.closest&&e.target.closest('.est');if(t)ir(+t.dataset.i,true);});
  document.addEventListener('keydown',function(e){
    if(e.target&&/^(INPUT|TEXTAREA)$/.test(e.target.tagName))return;
    if(e.key==='ArrowRight')ir(atual+1,true);
    if(e.key==='ArrowLeft')ir(atual-1,true);
  });
  var k0=0;
  var m=/^#d(\d+)$/.exec(location.hash||'');
  if(m){k0=Math.min(N-1,+m[1]);}
  else{try{var s=localStorage.getItem('om-degrau');if(s!==null)k0=Math.min(N-1,+s);}catch(e){}}
  ir(k0,false);
})();
