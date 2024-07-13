<script>
  // Layouts
  import LandingLeft from '@/layouts/StartLayout.vue'

  // UI elements
  import Button from '@/components/Button.vue'
  import Form from '@/components/Form.vue'

  export default {
    components: {
      // Layouts
      LandingLeft,

      // UI elements
      Button,
      Form
    },
    created() {
      document.title = this.$t('title.Login')

      if (localStorage.getItem('token')) {
        this.$router.push('/dashboard')
      }
    },
    data() {
      return {
        requestData: {
          username: '',
          password: ''
        },
        requestURL: 'https://chalk.fortheinternet.xyz/api/logins/logins.json',
        error: '',
        success: false
      }
    },
    methods: {
      handleResponse(data) {
        this.error = data.error || ''
        this.success = !this.error

        if (this.success) {
          localStorage.setItem('token', data.token)
          this.$router.push('/dashboard')
        }
      }
    }
  }
</script>

<template>
  <div id="wrapper">
    <LandingLeft view="Login" />
    <main>
      <article>
        <h4>{{ $t('text.heading.login-1') }}</h4>
        <p class="subtext">
          {{ $t('text.paragraph.login-1') }}
        </p>
      </article>

      <Form :requestURL :requestData ref="Form" @submitted="handleResponse">
        <form>
          <p class="mb-2 text-base font-bold">
            {{ $t('inputs.text.username') }}
          </p>

          <input
            v-model="requestData.username"
            :placeholder="$t('inputs.placeholders.username')"
            autocomplete="on"
            name="username"
            class="InputField"
          />

          <p class="mb-2 text-base font-bold">
            {{ $t('inputs.text.password') }}
          </p>

          <input
            v-model="requestData.password"
            :placeholder="$t('inputs.placeholders.password')"
            type="password"
            autocomplete="on"
            name="password"
            class="InputField"
          />
        </form>

        <p v-if="error" class="error">{{ $t(`errors.${error}`) }}</p>
        <p v-else-if="success" class="success">{{ $t('success') }}</p>

        <div class="button-row">
          <Button @click="this.$refs.Form.submitForm()" variant="highlighted">
            {{ $t('button.submit') }}
          </Button>
          <Button
            routePath="https://fortheinternet.notion.site/How-to-reset-a-password-b1092586c9fc4893b4d373dd4b94039c?pvs=4"
            variant="ghost"
          >
            {{ $t('button.forgot-password') }}
          </Button>
        </div>
      </Form>

      <article>
        <p class="subtext" v-html="$t('text.paragraph.policies')"></p>
      </article>
    </main>
  </div>
</template>
