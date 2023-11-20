// index.js

function deleteNote(noteId) {
  fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
  })
  .then((_res) => {
      window.location.href = "/";
  });
}

function editNote(noteId) {
  console.log(`Edit button clicked for note ID ${noteId}`);


  const newContent = prompt("Enter the new content for the note:");

  if (newContent !== null) {  // Check if the user clicked Cancel
      fetch(`/edit-note/${noteId}`, {
          method: "POST",
          headers: {
              "Content-Type": "application/x-www-form-urlencoded",
          },
          body: `new_content=${encodeURIComponent(newContent)}`,
      })
      .then((_res) => {
          window.location.href = "/";
      })
      .catch((error) => {
          console.error("Error editing note:", error);
      });
  }
}
