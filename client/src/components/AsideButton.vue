<script>
  export default {
    props: {
      routePath: '',
      internal: false
    },
    methods: {
      navigateToPage() {
        this.$router.push(this.routePath)
      }
    }
  }
</script>

<template>
  <div class="w-max cursor-default">
    <a @click="navigateToPage" v-if="internal" class="AsideItem cursor-pointer">
      <slot></slot>
    </a>

    <a :href="routePath" v-else class="AsideItem cursor-pointer">
      <slot></slot>
    </a>
  </div>
</template>
