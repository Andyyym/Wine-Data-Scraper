$(document).ready(function () {
  var resultArea = $("#output");
  var searchBar = $("#searchBar");
  var searchButton = $(".glyphicon-search");

  var displayResults = function () {

      $('#output').html('');

      var searchField = $('#searchBar').val();
      var expression = new RegExp(searchField, "i");
      $.getJSON('./Data/WineData.json', function (data) {
          $.each(data, function (key, value) {
              if (value.Name.search(expression) != -1) {
                  $('#output').append(`
          
              <div class="col-md-4">
              <a href=${value.URL}>
                  <div class="card" style="width: 18rem;" >
                  <img src="./Data/background.jpg" class="card-img-top" alt="...">
                      <div class="card-body">
                          <h5 class="card-title">${value.Name}</h5>
                          <h6 class="card-subtitle mb-2 text-muted">${value.Price} <br> ${value.Store}</br></h6>
                          <p class="card-text">${value.Deal}</p>
                       </div>
                  </div>
              </div>`)
              }
          })
      })
  }

      searchButton.click(function () {
          resultArea.empty();
          displayResults()
          $("#searchBox").animate({ 'padding-top': "0" }, 600);
          $(".container-fluid").animate({ height: "30vh" }, 600);
      });

      searchBar.keypress(function (e) {
          if(e.keyCode==13)
          $(searchButton).click();
      });
  })
