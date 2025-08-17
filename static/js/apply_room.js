
document.addEventListener("DOMContentLoaded", function () {
    console.log("apply_room.js loaded");
  
    const rooms = [
      {
        name: "Deluxe Room 1",
        block: "Block A",
        type: "Deluxe",
        residents: [
          { country: "Malaysia", flag: "my", course: "Software Engineering" },
          { country: "India", flag: "in", course: "Information Systems" },
          { country: "China", flag: "cn", course: "Software Engineering" }
        ]
      },
      {
        name: "Deluxe Room 2",
        block: "Block B",
        type: "Deluxe",
        residents: [
          { country: "Pakistan", flag: "pk", course: "Information Systems" }
        ]
      },
      {
        name: "Deluxe Room 3",
        block: "Block C",
        type: "Deluxe",
        residents: []
      },
      {
        name: "Premium Room 1",
        block: "Block A",
        type: "Premium",
        residents: [
          { country: "Indonesia", flag: "id", course: "Software Engineering" },
          { country: "Bangladesh", flag: "bd", course: "Information Systems" }
        ]
      },
      {
        name: "Premium Room 2",
        block: "Block B",
        type: "Premium",
        residents: []
      },
      {
        name: "Premium Room 3",
        block: "Block C",
        type: "Premium",
        residents: []
      }
    ];
  
    function filterRooms() {
      const selectedType = document.getElementById('roomType').value;
      const selectedBlock = document.getElementById('preferredBlock').value;
      const deluxeRoomList = document.getElementById('deluxeRoomList');
      const premiumRoomList = document.getElementById('premiumRoomList');
  
      deluxeRoomList.innerHTML = "";
      premiumRoomList.innerHTML = "";
  
      const selectedRoom = sessionStorage.getItem("selectedRoom") ? JSON.parse(sessionStorage.getItem("selectedRoom")) : null;
  
      rooms.forEach(room => {
        if (selectedType && room.type !== selectedType) return;
        if (selectedBlock && room.block !== selectedBlock) return;
  
        const li = document.createElement('li');
        li.className = "list-group-item";
  
        const residentsInfo = room.residents.length > 0
          ? `<strong>Residents (${room.residents.length}/4):</strong><br>` +
            room.residents.map(r =>
              `<span class="flag-icon flag-icon-${r.flag} me-2"></span>${r.country} - ${r.course}`
            ).join("<br>")
          : "<em>No residents yet</em>";
  
        li.innerHTML = `
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <strong>${room.name}</strong> - ${room.block}<br>
              ${residentsInfo}
            </div>
            <div>
              <button type="button" class="btn btn-outline-primary btn-sm">
                <i class="bi bi-check2-square"></i> Select
              </button>
            </div>
          </div>
        `;
  
        const selectBtn = li.querySelector("button");
        selectBtn.addEventListener('click', () => {
          alert(`${room.name} selected. Now press "Apply Now" to confirm.`);
          sessionStorage.setItem("selectedRoom", JSON.stringify(room));
          document.querySelectorAll('.list-group-item').forEach(item => item.classList.remove('selected-room'));
          li.classList.add('selected-room');
        });
  
        if (selectedRoom && selectedRoom.name === room.name && selectedRoom.block === room.block && selectedRoom.type === room.type) {
          li.classList.add('selected-room');
        }
  
        (room.type === "Deluxe" ? deluxeRoomList : premiumRoomList).appendChild(li);
      });
    }
  
    // Initial render
    filterRooms();
  
    // Event listeners
    document.getElementById('roomType').addEventListener('change', filterRooms);
    document.getElementById('preferredBlock').addEventListener('change', filterRooms);
  
    document.getElementById('applyRoomForm').addEventListener('submit', function (event) {
      event.preventDefault();
      const selected = sessionStorage.getItem("selectedRoom");
      if (!selected) {
        alert("Please select a room before applying.");
        return;
      }
      window.location.href = './confirmation.html';
    });
  
    // function toggleSidebar() {
    //   document.getElementById('sidebar').classList.toggle('active');
    //   document.getElementById('main-content').classList.toggle('active');
    // }
  
    // window.toggleSidebar = toggleSidebar;
  
    // const currentPage = window.location.pathname.split('/').pop().toLowerCase();
    // document.querySelectorAll('#sidebar a').forEach(link => {
    //   const linkHref = link.getAttribute('href').split('/').pop().toLowerCase();
    //   if (linkHref === currentPage) {
    //     link.classList.add('active');
    //   }
    // });
  });
  