<template>
  <div>
    <h2>Category Management</h2>
    <button @click="exportcsv">Download Report</button>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search Categories"
      @input="filterCategories"
    />

    <form @submit.prevent="addCategory">
      <input
        type="text"
        v-model="newCategoryName"
        placeholder="New Category Name"
        required
      />
      <button type="submit">Add Category</button>
    </form>

    <table v-if="filteredCategories.length > 0">
      <thead>
        <tr>
          <th>Id</th>
          <th>Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="category in filteredCategories" :key="category.id">
          <td>
            <input
              type="text"
              v-model="category.name"
              :disabled="category.id !== editingCategoryId"
            />
          </td>
          <td>
            <button
              v-if="category.id !== editingCategoryId"
              @click="startEditing(category)"
            >
              Edit
            </button>
            <button v-else @click="saveCategory(category)">Save</button>
            <button @click="deleteCategory(category)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else>
      <p>No categories found</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      categories: [],
      newCategoryName: "",
      editingCategoryId: null,
      filteredCategories: [],
    };
  },
  mounted() {
    this.loadCategories();
  },
  methods: {
    async loadCategories() {
      try {
        const response = await axios.get("/categories");

        this.categories = response.data;
        this.filteredCategories = this.categories;
      } catch (error) {
        console.error("Error loading categories:", error);
      }
    },
    filterCategories() {
      const query = this.searchQuery.toLowerCase();
      this.filteredCategories = this.categories.filter((category) =>
        category.name.toLowerCase().includes(query)
      );
    },
    async addCategory() {
      try {
        const response = await axios.post("/categories", {
          name: this.newCategoryName,
        });
        console.log("Category added:", response.data);
        this.newCategoryName = "";
        this.loadCategories();
      } catch (error) {
        console.error("Error adding category:", error);
      }
    },
    startEditing(category) {
      this.editingCategoryId = category.id;
    },
    exportcsv() {
      axios.post("/export/1", {}, { responseType: "blob" }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const downloadLink = document.createElement("a");
        downloadLink.href = url;
        downloadLink.setAttribute("download", "report.csv");
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      });
    },
  },
};
</script>
