<script>
  import axios from 'axios'

  export default {
    props: {
      requestURL: '',
      requestData: {}
    },
    emits: ['submitted'],
    methods: {
      async submitForm() {
        try {
          const response = await axios.post(this.requestURL, this.requestData)
          console.log(response.data)

          this.$emit('submitted', response.data)
        } catch (error) {
          if (error.response) {
            console.table({
              'Error code': error.response.data.error,
              'Error message': error.response.data.message
            })

            this.$emit('submitted', error.response.data)
          } else {
            console.log('Something happened.' + error)
          }
        }
      }
    }
  }
</script>

<template>
  <div class="FormInputs-wrapper">
    <slot></slot>
  </div>
</template>

<style scoped>
  .FormInputs-wrapper {
    @apply mb-4 w-full select-none;
  }
</style>
