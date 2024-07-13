<script>
  export default {
    props: {
      routePath: ''
    },
    methods: {
      navigateToPage() {
        if (this.routePath) {
          if (this.routePath.startsWith('https://')) {
            window.location.href = this.routePath
          } else {
            this.$router.push(this.routePath)
          }
        }
      }
    }
  }
</script>

<template>
  <div class="w-max cursor-default">
    <button @click="navigateToPage" class="AsideItem cursor-pointer">
      <slot></slot>
    </button>
  </div>
</template>
