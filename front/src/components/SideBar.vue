<template id="sidebar">
  <div>
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion toggled" id="accordionSidebar">

      <router-link class="sidebar-brand d-flex align-items-center justify-content-center" to="/projects">
          <div class="sidebar-brand-icon rotate-n-15">
              <i class="fas fa-laugh-wink"></i>
          </div>
          <div class="sidebar-brand-text mx-3">DL Framework<sup>2</sup></div>
      </router-link>


      <!-- Divider -->
      <hr class="sidebar-divider my-0">
      <hr class="sidebar-divider">

      <!-- Nav Item - Dashboard -->
      <li class="nav-item active">
        <router-link class="nav-link" to="/projects">
          <i class="fas fa-fw fa-store"></i>
          <span>Projects</span>
        </router-link>
      </li>

      <li class="nav-item active">
        <router-link class="nav-link" to="/users">
          <i class="fas fa-fw fa-tasks"></i>
          <span>Users</span>
        </router-link>
      </li>
    </ul>
  </div>
</template>