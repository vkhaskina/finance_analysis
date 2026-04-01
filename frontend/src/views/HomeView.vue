<template>
  <div class="app-container">
      <div class="main-panel">
        <h3>Загрузите CSV-файл</h3>

        <form @submit.prevent="submitForm" enctype="multipart/form-data">
          <input
            type="file"
            id="myFile"
            ref="fileInput"
            accept=".csv"
            @change="handleFileChange"
          >
          <button type="submit">Загрузить</button>

          <div v-if="loading" class="loading">
            <div class="loading-spinner"></div>
            <div>Идет загрузка...</div>
          </div>

          <div v-if="error" class="error">
            {{ error }}
          </div>

          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
        </form>
      </div>
  </div>
</template>

<script>
  export default {
    name: 'HomeView',

    data(){
      return {
        selectedFile: null,
        loading: false,
        error: null,
        successMessage: null,
      }
    },

    methods: {
      handleFileChange(event) {
        this.selectedFile = event.target.files[0];

        if (this.selectedFile && !this.selectedFile.name.endsWith('.csv')) {
          this.error = 'Пожалуйста, выберите CSV-файл';
          this.selectedFile = null;
          return;
        }
        this.error = null;
      },

      async submitForm() {
        if (!this.selectedFile) {
          this.error = 'Пожалуйста, выберите файл';
          return;
        }

        const formData = new FormData();
        formData.append('csv_file', this.selectedFile);

        this.loading = true;
        this.error = null;
        this.successMessage = null;

        try {
          const response = await fetch('http://localhost:8000/api/upload/', {
            method: 'POST',
            body: formData,
            credentials: 'include',
          });

          const result = await response.json();
          console.log('Ответ от сервера:', result);

          if (response.ok) {
            this.successMessage = 'Файл успешно загружен!';

            if (this.$refs.fileInput) {
              this.$refs.fileInput.value = '';
            }
            this.selectedFile = null;

          } else {
            this.error = result.error || result.message || 'Ошибка при загрузке файла';
          }
        } catch (err) {
          this.error = 'Ошибка сети или сервера: ' + err.message;
          console.error('Ошибка:', err);
        } finally {
          this.loading = false;
        }
      },
    }
  }
</script>

<style>
  .app-container {
    max-width: 100%;
    margin: 0 auto;
    padding: 10px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f5f5f5;
    place-items: center;
  }


  .main-panel {
    background: #f5f5f5;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    max-width: 500px;
    margin: 0 auto;
  }

  input[type="file"] {
    padding: 12px;
    border: 2px dashed #3498db;
    border-radius: 8px;
    cursor: pointer;
    background: white;
    transition: all 0.3s;
  }

  input[type="file"]:hover {
    border-color: #2980b9;
    background: #f8f9fa;
  }

  button {
    padding: 12px 24px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
    transition: all 0.3s;
    margin-top: 10px;
  }

  button:hover {
    background: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 5px 10px rgba(0,0,0,0.2);
  }

  button:disabled {
    background: #cccccc;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
</style>
