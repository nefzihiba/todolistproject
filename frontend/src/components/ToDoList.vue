<template>
  <div class="prin">
    <h1>Ma Todoliste</h1>

    <input
      class="search"
      v-model="searchTerm"
      @input="filterTasks"
      placeholder="Rechercher par titre"
    />

    <div>
      <input
        class="ajoutertask"
        v-model="newTask"
        @keyup.enter="addTask"
        placeholder="Ajouter une tâche"
      />
      <button class="ajouter" @click="addTask">Ajouter</button>
    </div>

    <ul>
      <li v-for="(task, index) in paginatedTasks" :key="task.id">
        <input class="newtask" type="checkbox" v-model="task.completed" @change="modifyTask(task)">
        <span>{{ task.title }}</span>
        <button class="modifier" @click="openModal(task)">Modifier</button>
        <button class="supprimer" @click="removeTask(task.id, index)">Supprimer</button>
      </li>
    </ul>

    <pagination :totalPages="totalPages" :currentPage="currentPage" @page-changed="changePage" />
  
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <input v-model="editedTaskTitle" placeholder="Modifier la tâche">
        <button class="enregistrer" @click="saveEditedTask">Enregistrer</button>
        <button class="Annuler" @click="cancelEdit">Annuler</button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue';
import Pagination from './Pagination.vue';

const newTask = ref('');
const tasks = ref([]);
const editedTaskTitle = ref('');
const showModal = ref(false);
let currentTask = null;


const itemsPerPage = 5; 

const currentPage = ref(1);

const totalPages = computed(() => Math.ceil(tasks.value.length / itemsPerPage));

const searchTerm = ref('');

const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    return task.title.toLowerCase().includes(searchTerm.value.toLowerCase());
  });
});

const paginatedTasks = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  return filteredTasks.value.slice(startIndex, endIndex); 
});
const fetchTasks = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/Apitodo/tasks/");
    const data = await response.json();
    tasks.value = data.map(task => ({ ...task, editing: false, newTitle: '' }));
  } catch (error) {
    console.error("Erreur lors de la récupération des tâches:", error);
  }
};

const addTask = async () => {
  if (!newTask.value.trim()) {
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/Apitodo/tasks/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title: newTask.value, completed: false }),
    });

    if (response.ok) {
      const data = await response.json();
      tasks.value.push(data);
      newTask.value = "";
    } else {
      console.error("Erreur lors de l'ajout de la nouvelle tâche:", response.statusText);
    }
  } catch (error) {
    console.error("Erreur lors de l'ajout de la nouvelle tâche:", error);
  }
};

const removeTask = async (taskId, index) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/Apitodo/tasks/${taskId}/delete/`, {
      method: 'DELETE',
    });

    if (response.ok) {
      tasks.value.splice(index, 1);
    } else {
      console.error(`Erreur lors de la suppression de la tâche avec l'ID ${taskId}. Statut : ${response.statusText}`);
    }
  } catch (error) {
    console.error(`Erreur lors de la suppression de la tâche avec l'ID ${taskId}:`, error);
  }
};

const modifyTask = async (task) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/Apitodo/tasks/${task.id}/update/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(task),
    });

    if (!response.ok) {
      console.error(`Erreur lors de la modification de la tâche avec l'ID ${task.id}. Statut : ${response.statusText}`);
    }
  } catch (error) {
    console.error(`Erreur lors de la modification de la tâche avec l'ID ${task.id}:`, error);
  }
};

const openModal = (task) => {
  currentTask = task;
  editedTaskTitle.value = task.title;
  showModal.value = true;
};

const saveEditedTask = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/Apitodo/tasks/${currentTask.id}/update/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title: editedTaskTitle.value }),
    });

    if (response.ok) {
      currentTask.title = editedTaskTitle.value;
      showModal.value = false;
    } else {
      console.error(`Erreur lors de la modification du titre de la tâche avec l'ID ${currentTask.id}. Statut : ${response.statusText}`);
    }
  } catch (error) {
    console.error(`Erreur lors de la modification du titre de la tâche avec l'ID ${currentTask.id}:`, error);
  }
};

const cancelEdit = () => {
  showModal.value = false;
};



const changePage = (page) => {
  currentPage.value = page;
};

onMounted(() => {
  fetchTasks();
});
</script>


<style scoped>
.prin{
 height: max-content;   
 width: 700px;
 position: relative;
 top: 100px;
}
.newtask{
    position: relative;
    right: 200px;
    top: 10px;
}

div {
    background-color: #f8f9fa;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    border-radius: 8px;
    width: 600px;
    text-align: center;
    margin: auto;
}

h1 {
    color: #343a40;
    font-size: 24px;
}

input {
    padding: 10px;
    margin-bottom: 15px;
    width: 70%;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 14px;
    margin-right: 6px;
}

.ajouter {
    padding: 10px;
    cursor: pointer;
    width: 25%;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

.ajouter:hover {
    background-color: #0056b3;
}

ul {
    list-style: none;
    padding: 0;
}

li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #ced4da;
    margin-bottom: 8px;
    font-size: 16px;
}

li:hover {
    background-color: #f0f0f0;
    transition: background-color 0.3s ease;
}
span{
    position: relative;
    right: 400px;
    top: 2px;
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-size: 1.rem;

}


.supprimer {
    background-color: #dc3545;
    color: #fff;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

.modifier {
    background-color: #339256;
    color: #fff;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
    position: relative;
    right: 10px;
}

.supprimer {
    background-color: #c82333;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-content input {
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}


.enregistrer {
  padding: 8px 16px;
  margin-right: 10px;
  margin-top: 10px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  background-color:  #339256;
  color: #fff;
  transition: background-color 0.3s ease;
}

.Annuler {
  padding: 8px 16px;
  margin-right: 10px;
  margin-top: 10px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  background-color:  #c82333;
  color: #fff;
  transition: background-color 0.3s ease;
}




</style>