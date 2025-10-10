<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">
        Login
        <i class="bi bi-door-open-fill"></i>
      </button>
    </form>
    <div v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post("/login", {
          username: this.username,
          password: this.password,
        });
        const { access_token, user_info } = response.data;
        console.log(user_info);
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("user", JSON.stringify(user_info));

        if (user_info.role === "admin") {
          this.$router.push("/admin_dashboard");
        } else {
          this.$router.push("/dashboard");
        }
      } catch (error) {
        this.errorMessage = "Login failed. Please try again.";
      }
    },
  },
};
</script>

<style scoped></style>
