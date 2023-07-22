$(document).ready(function () {
    var resultArea = $("#output");
    var searchBar = $("#searchBar");
    var searchButton = $(".glyphicon-search");
  
    var displayResults = function () {
        var searchField = searchBar.val();
        var expression = new RegExp(searchField, "i");
        $.getJSON('./Data/PnP.json', function (data) {
            var filtered = data.filter(function (value) {
                return value.Name.search(expression) != -1;
            });
            render(filtered);
        });
    }
  
    var render = function (items) {
        resultArea.empty();
        items.forEach(function (value) {
            resultArea.append(`
            <div class="col-md-4">
            <a href=${value.URL}>
                <div class="card" style="width: 18rem;" >
                <img src=${value.Image} class="card-img-top" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">${value.Name}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">${value.Price} <br> ${value.Store}</br></h6>
                        <p class="card-text">${value.Deal}</p>
                     </div>
                </div>
            </div>`);
        });
    };
  
    var onSearch = function () {
        displayResults();
        $("#searchBox").animate({ 'padding-top': "0" }, 600);
        $(".container-fluid").animate({ height: "30vh" }, 600);
    }
  
    searchButton.click(onSearch);
    searchBar.keypress(function (e) {
        if(e.keyCode==13)
        $(searchButton).click();
    });
  
    displayResults(); // Initial load
  });
  