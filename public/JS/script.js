 // Fetch data from API
 fetch('http://localhost:3000/api/wines')
 .then(response => response.json())
 .then(data => {
    // Display each product in a container
    const productContainer = document.getElementById('productContainer');
    let filteredData = data;

    function renderProducts() {
       productContainer.innerHTML = '';

       filteredData.forEach(product => {
          const productElement = document.createElement('div');
          productElement.classList.add('product');

          // Store name
          const storeName = document.createElement('p');
          storeName.textContent = 'Store: ' + product.StoreName;
          productElement.appendChild(storeName);

          // Item name
          const itemName = document.createElement('p');
          itemName.textContent = 'Item: ' + product.ItemName;
          productElement.appendChild(itemName);

          // Price
          const price = document.createElement('p');
          price.textContent = 'Price: ' + product.Price;
          productElement.appendChild(price);

          // Promotion message and end date
          if (product.OnPromotion) {
             const promotionMessage = document.createElement('p');
             promotionMessage.textContent = 'Promotion: ' + product.PromotionMessage;
             productElement.appendChild(promotionMessage);

             const promotionEndDate = document.createElement('p');
             promotionEndDate.textContent = 'Promotion End Date: ' + product.PromotionEndDate;
             productElement.appendChild(promotionEndDate);
          }

          // Image
          const image = document.createElement('img');
          image.src = product.Image;
          productElement.appendChild(image);

          productContainer.appendChild(productElement);
       });
    }

    function search() {
       const searchInput = document.getElementById('searchInput');
       const searchTerm = searchInput.value.toLowerCase();

       filteredData = data.filter(product => product.ItemName.toLowerCase().includes(searchTerm));
       renderProducts();
    }

    function filterPromotions() {
       filteredData = data.filter(product => product.OnPromotion);
       renderProducts();
    }

    const searchButton = document.getElementById('searchButton');
    searchButton.addEventListener('click', search);

    const promotionButton = document.getElementById('promotionButton');
    promotionButton.addEventListener('click', filterPromotions);

    renderProducts();
 })
 .catch(error => {
    console.error('Error:', error);
 });