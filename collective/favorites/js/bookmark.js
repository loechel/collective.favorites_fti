$(document).ready(function(){
  $("#document-action-addbrowserfavorite a").click(function(e){
    e.preventDefault(); // this will prevent the anchor tag from going the user off to the link
    
    if (document.all && window.external) {
      window.external.AddFavorite (window.location,document.title);
    }
    else if (window.sidebar) { 
      window.sidebar.addPanel(document.title,window.location,'');
    } 
    else {         
      var evt = jQuery.Event("keypress");
      evt.keyCode = 68; // d
      evt.ctrlKey = true;
      $(document).trigger(evt);
      alert (''
       +'Cannot programmatically add bookmarks!\n'
       +'Please press Ctrl+D to bookmark this page.'
      );
    }
  });
});
