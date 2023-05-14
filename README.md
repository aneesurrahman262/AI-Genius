<!DOCTYPE html>
<html>
<head>
  <title>Multimodal AI Story Teller</title>
  <style>
    /* Add your custom CSS styles here */
    body {
      font-family: Arial, sans-serif;
    }
    
    h1 {
      color: #FF0000;
    }
    
    .form-container {
      max-width: 400px;
      margin: 0 auto;
    }
    
    .form-group {
      margin-bottom: 20px;
    }
    
    .form-label {
      display: block;
      font-weight: bold;
    }
    
    .form-input {
      width: 100%;
      padding: 8px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    
    .form-button {
      padding: 10px 20px;
      font-size: 16px;
      background-color: #4CAF50;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    
    .form-button:hover {
      background-color: #45a049;
    }
  </style>
</head>
<body>
  <h1>Multimodal AI Story Teller</h1>
  <div class="form-container">
    <form id="story-form">
      <div class="form-group">
        <label class="form-label" for="prompt">Enter a story prompt:</label>
        <textarea class="form-input" id="prompt" rows="4" required></textarea>
      </div>
      <div class="form-group">
        <button class="form-button" type="submit">Generate Story</button>
      </div>
    </form>
    <div id="story-output"></div>
  </div>

  <script>
    // Add your JavaScript code here
    const form = document.getElementById('story-form');
    const storyOutput = document.getElementById('story-output');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const prompt = document.getElementById('prompt').value;
      
      // Send the prompt to the server API and retrieve the generated story
      const response = await fetch('/generate-story', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });
      
      const data = await response.json();
      
      // Display the generated story on the webpage
      if (data.story) {
        storyOutput.textContent = data.story;
      } else {
        storyOutput.textContent = 'Unable to generate the story. Please try again.';
      }
    });
  </script>
</body>
</html>
