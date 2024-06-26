<script>
// Menus
import LandingMenu from '@/components/menus/LandingMenu.vue'

// UI elements
import ChipButton from '@/components/elements/ChipButton.vue';
import FormInputs from '@/components/elements/FormInputs.vue';

export default {
  components: {
    // Menus
    LandingMenu,

    // UI elements
    ChipButton,
    FormInputs
  },
  created() {
    document.title = this.$t('title.Login')
  },
  data() {
    return {
      formData: {
        username: '',
        password: ''
      },
      formURL: "https://chalk.fortheinternet.xyz/api/logins/logins.json"
    }
  },
  methods: {
    handleResponse() {
      console.log('HandleResponse in Parent Component')
    }
  }
};
</script>

<template>
  <LandingMenu view="Login"/>
  <main>
    <article>
      <h4>{{ $t('text.heading.login-1') }}</h4>
      <p class="dark:text-opacity-55 text-opacity-55 dark:text-white text-black">{{ $t('text.paragraph.login-1') }}</p>
    </article>

    <FormInputs :formURL :formData ref="FormInputs">
      <form>
        <input v-model="formData.username" :placeholder="$t('inputs.placeholders.username')" autocomplete="on" name="username"></input>
        <input v-model="formData.password" :placeholder="$t('inputs.placeholders.password')" type="password" autocomplete="on" name="password"></input>
      </form>
      
      <div class="flex sm:flex-row flex-col">
        <ChipButton @click="this.$refs.FormInputs.submitForm()" :highlighted="true">{{ $t('button.submit') }}</ChipButton>
        <ChipButton routePath="https://fortheinternet.notion.site/How-to-reset-a-password-b1092586c9fc4893b4d373dd4b94039c?pvs=4" :internal="false">{{ $t('button.forgot-password') }}</ChipButton>
      </div>
    </FormInputs>

  </main>
</template>