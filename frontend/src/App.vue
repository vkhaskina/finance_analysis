<template>

  <div id="wrapper">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">

        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbar-menu" class="navbar-menu">
        <div class="navbar-start">
          <router-link
            to="/"
            class="navbar-item"
            :class="{ 'is-active': $route.path === '/'}">
            Главная
          </router-link>

        </div>

        <!-- <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <a class="button is-primary">
                <strong>Sign up</strong>
              </a>
              <a class="button is-light">
                Log in
              </a>
            </div>
          </div>
        </div> -->
      </div>
    </nav>

    <section class="section">
      <div class="container">
        <router-view/>
      </div>
    </section>
  </div>


</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style>
  @import "bulma/css/bulma.min.css";
  html, body {
    margin: 0;
    padding: 0;
    width: 100%;
  }

  #app, #wrapper {
    width: 100%;
    min-height: 100vh;
    display: flex;
    padding: 0;
    margin: 0;
    flex-direction: column;
  }

  .navbar {
    width: 100%;
    padding: 0;
    margin: 0;
    border-radius: 0;
  }

  .navbar-item {
    background-color: black;
  }

  .section {
    width: 100%;
    padding-left: 0;
    padding-right: 0;
    flex: 1;
    padding-top: 3.25rem;
    background: #f5f5f5;
  }
</style>
