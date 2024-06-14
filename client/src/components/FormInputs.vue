<script>
import axios from "axios";

export default {
  props: {
    formURL: String,
    formData: Object
  },
  data() {
    return {
      responseData: Object
    }
  },
  methods: {
    async submitForm() {
      console.log("[cast] Submitting form:", this.formData);

      
      const { response } = await axios.post(this.formURL, this.formData)

      this.responseData = response
      


    }
  }
};
</script>

<template>
  <slot name="inputs"></slot>
  <slot name="buttons"></slot>
</template>

<style scoped>

template {
  @apply w-full mb-4 select-none;
}

</style>
