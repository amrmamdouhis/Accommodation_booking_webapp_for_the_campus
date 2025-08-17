document.addEventListener("DOMContentLoaded", function () {
  console.log("apply_room.js loaded");

  const rooms = [ /* Your room data here (unchanged) */ ];

  function filterRooms() {
    const selectedType = document.getElementById('roomType').value;
    const selectedBlock = document.getElementById('preferredBlock').value;
    const deluxeRoomList = document.getElementById('deluxeRoomList');
    const premiumRoomList = document.getElementById('premiumRoomList');

    deluxeRoomList.innerHTML = "";
    premiumRoomList.innerHTML = "";

    const selectedRoom = sessionStorage.getItem("selectedRoom")
      ? JSON.parse(sessionStorage.getItem("selectedRoom"))
      : null;

    rooms.forEach(room => {
      if (selectedType && room.type !== selectedType) return;
      if (selectedBlock && room.block !== selectedBlock) return;

      const li = document.createElement('li');
      li.className = "list-group-item";

      const residentsInfo = room.residents.length > 0
        ?` <strong>Residents (${room.residents.length}/4):</strong><br>` +
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

      if (selectedRoom &&
        selectedRoom.name === room.name &&
        selectedRoom.block === room.block &&
        selectedRoom.type === room.type) {
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

    const selectedRoom = JSON.parse(selected);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("/apply-room/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify({
        room_name: selectedRoom.name,
        block: selectedRoom.block,
        type: selectedRoom.type
      })
    })
    .then(response => {
      if (response.ok) {
        sessionStorage.removeItem("selectedRoom");
        return response.json();
      } else {
        throw new Error("Room booking failed.");
      }
    })
    .then(data => {
      alert("Room successfully applied! Redirecting...");
      window.location.href = data.redirect_url || "/student/profile/";
    })
    .catch(error => {
      alert("Error: " + error.message);
    });
  });
});