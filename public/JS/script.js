$(document).ready(function(){
    $.ajaxSetup({ cache: false });
    $('#search').keyup(function(){
     $('#result').html('');
     $('#state').val('');
     var searchField = $('#search').val();
     var expression = new RegExp(searchField, "i");
     $.getJSON('./WineData.json', function(data) {
      $.each(data, function(key, value){
       if (value.Name.search(expression) != -1)
       {
       
         // $('#result').append('<li class="list-group-item link-class">'+value.Name+' \n| '+value.Price+' | \n<span class="text-muted">'+value.Deal+'</span> | <a href='+value.URL+'>'+value.Store+'</a>');
         
         $('#result').append(`
         <div class="row">
         <div class="col s12">
           <div class="card  grey darken-4 darken-1">
             <div class="card-content white-text">
               <h4 class="card-title m1">${value.Name} (${
              value.Price
            })<span class="blue-text m-4"> ${value.Deal}</span></h4>
            <div class="card-action">
            <a href=${value.URL}>${value.Store}</a>
          </div>
             </div>
           </div>
         </div>
       </div>
         `) 
      }
      });   
     });
    });
    
    $('#result').on('click', '.list-group-item', function(e){
       var click_text = $(this).text();
       $('#search').val(click_text[0]);
       $("#result").html(this);
    });
   });