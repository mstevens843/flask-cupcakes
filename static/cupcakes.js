$(document).ready(function() {
    // Function to create HTML for cupcake
    function generateCupcakeHTML(cupcake) {
        const image = cupcake.image || 'https://tinyurl.com/demo-cupcake';
        return `
            <li data-cupcake-id="${cupcake.id}" class="cupcake-item">
                <img src="${image}" alt="${cupcake.flavor}" style="width: 100px; height: 100px;">
                <span>${cupcake.flavor} - ${cupcake.size} - Rating: ${cupcake.rating}</span>
            </li>
        `;
    }

    // Load cupcakes when the page loads
    async function loadCupcakes() {
        const response = await axios.get('/api/cupcakes');
        const cupcakes = response.data.cupcakes;

        $('#cupcakes-list').empty(); // Clear existing list before appending
        for (let cupcake of cupcakes) {
            $('#cupcakes-list').append(generateCupcakeHTML(cupcake));
        }
    }

    loadCupcakes();

    // Handle form submission to add new cupcake
    $('#cupcake-form').on('submit', async function(e) {
        e.preventDefault();

        const flavor = $('#flavor').val();
        const size = $('#size').val();
        const rating = $('#rating').val();
        const image = $('#image').val() || null; // Use null if no image is provided

        const response = await axios.post('/api/cupcakes', {
            flavor, 
            size,
            rating,
            image
        });

        const newCupcake = response.data.cupcake;

        // Append new cupcake to the list without reloading
        $('#cupcakes-list').append(generateCupcakeHTML(newCupcake));

        // Reset the form after submission
        $('#cupcake-form').trigger('reset');
    });

    // Handle click on cupcake to show details in the details-popup
    $('#cupcakes-list').on('click', '.cupcake-item', function(e) {
        const $cupcake = $(e.target).closest('li');
        const cupcakeId = $cupcake.attr('data-cupcake-id');

        // Get cupcake details from API
        axios.get(`/api/cupcakes/${cupcakeId}`)
            .then(response => {
                const cupcake = response.data.cupcake;

                // Populate details-popup with cupcake details
                $('#popup-flavor').val(cupcake.flavor);
                $('#popup-size').val(cupcake.size);
                $('#popup-rating').val(cupcake.rating);
                $('#popup-image').val(cupcake.image);
                $('#popup-cupcake-id').val(cupcake.id);

                // Show the details-popup
                $('#details-popup').show();
            });
    });

    // Handle update cupcake form submission in details-popup
    $('#popup-update-form').on('submit', async function(e) {
        e.preventDefault();

        const cupcakeId = $('#popup-cupcake-id').val();
        const flavor = $('#popup-flavor').val();
        const size = $('#popup-size').val();
        const rating = $('#popup-rating').val();
        const image = $('#popup-image').val() || null;

        await axios.patch(`/api/cupcakes/${cupcakeId}`, {
            flavor, size, rating, image
        });

        // Reload cupcakes after update
        loadCupcakes();
        $('#details-popup').hide();
    });

    // Handle delete cupcake from details-popup
    $('#popup-delete').on('click', async function() {
        const cupcakeId = $('#popup-cupcake-id').val();
        await axios.delete(`/api/cupcakes/${cupcakeId}`);

        // Reload cupcakes after deletion
        loadCupcakes();
        $('#details-popup').hide();
    });

    // Hide details-popup when clicking outside of it
    $(window).on('click', function(e) {
        if ($(e.target).is('#details-popup')) {
            $('#details-popup').hide();
        }
    });
});
