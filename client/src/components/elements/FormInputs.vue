<script>
import axios from "axios";

export default {
  props: {
    formURL: String,
    formData: Object
  },
  emits: ['submitted'],
  methods: {
    async submitForm() {
      try {
        const response = await axios.post(this.formURL, this.formData)
        console.log(response.data)
      }

      catch (error) {
        console.table({
          'Error code': error.response.data.error,
          'Error message': error.response.data.message
        })
      }

      this.$emit('submitted', this.responseData)
    }
  }
};
</script>

<template>
  <div class="FormInputs-wrapper">
    <slot></slot>
  </div>
</template>

<style scoped>

.FormInputs-wrapper {
  @apply w-full mb-4 select-none;
}

</style>