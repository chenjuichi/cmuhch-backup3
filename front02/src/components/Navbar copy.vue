<template>
  <div class="navbar">
      <nav class="navbar custom-nav fixed-top navbar-expand-lg navbar-light bg-light">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
 
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" class="nav-link">About</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/products" class="nav-link">Products</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/news" class="nav-link">News</router-link>
            </li>
<!--
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Dropdown link
              </a>
              <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">

                <div class="nav-item-drawer">
                  <router-link
                    v-for="subLink in subLinks"
                    :key="subLink.id"
                    :to="`${subLink.page}`"
                  >
                  {{ subLink.text }}
                  </router-link>
                </div>
              </div>
            </li>
-->
            <li class="dropdown">
              <a id="drop1" href="#" role="button" class="dropdown-toggle" data-toggle="dropdown">
                Dropdown <b class="caret"></b>
              </a>
              <ul class="dropdown-menu" role="menu" aria-labelledby="dLabel">
                <li><a tabindex="-1" href="#">Action</a></li>
                <li><a tabindex="-1" href="#">Another action</a></li>
                <li><a tabindex="-1" href="#">Something else here</a></li>
                <li class="divider"></li>
                <li><a tabindex="-1" href="#">Separated link</a></li>
              </ul>
            </li>




            </ul>
        </div>
    </nav>
  </div>
</template>
 
<script>
export default {
  name: 'Navbar',
  props: {
    msg: String
  },

  data() {
    return {
      subLinks: [
        {
          id: 0,
          text: 'Buy Sublink 1',
          page: '/Buy-more'
        },
        {
          id: 1,
          text: 'Buy Sublink 2',
          page: '/Buy-less'
        },
      ]
    };
  },
}
</script>
 
<style scoped lang="scss">
  @media (min-width: 992px) { 
    .navbar.custom-nav{
      padding-top:16px;
      padding-bottom:16px;
      background-color: #7DA79D !important;
    }
   }
</style>