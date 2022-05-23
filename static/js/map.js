// check if we have lat and log 
console.log(lt, lg, parseFloat(lg));
if (lt && lg){
    console.log(lt, lg, parseFloat(lg));
    let map;

    function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: parseFloat(lt), lng: parseFloat(lg) },
        zoom: 10,
    });
    }

    window.initMap = initMap;

    for (let i = 0; i < data.length; i++) {
        console.log(data[i]);   
    }
    //markers
    // data.map((position) => {
        // console.log(position);
        // const marker = new google.maps.Marker({
        //     position,
        //     map:map
        // })
        
    // })
}