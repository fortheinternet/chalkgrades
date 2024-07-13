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
      document.title = this.$t('title.Signup')

      if (localStorage.getItem('token')) {
        this.$router.push('/dashboard')
      }
    },
    data() {
      return {
        requestData: {
          username: '',
          password: '',
          password_confirm: '',
          access_code: ''
        },
        requestURL: 'https://chalk.fortheinternet.xyz/api/logins/signups.json',
        error: '',
        success: false
      }
    },
    methods: {
      handleResponse(data) {
        this.error = data.error || ''
        this.success = !this.error

        if (this.success) {
          this.$router.push('/dashboard')
        }
      }
    }
  }
</script>

<template>
  <div id="wrapper">
    <LandingLeft view="Signup" />
    <main>
      <article>
        <h4>{{ $t('text.heading.signup-1') }}</h4>
        <p class="subtext">
          {{ $t('text.paragraph.signup-1') }}
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
            name="username"
            class="InputField"
          />

          <p class="mb-2 text-base font-bold">
            {{ $t('inputs.text.new-password') }}
          </p>

          <input
            v-model="requestData.password"
            :placeholder="$t('inputs.placeholders.new-password')"
            name="new_password"
            class="InputField"
          />

          <p class="mb-2 text-base font-bold">
            {{ $t('inputs.text.password-confirm') }}
          </p>

          <input
            v-model="requestData.password_confirm"
            :placeholder="$t('inputs.placeholders.password-confirm')"
            name="password_confirm"
            class="InputField"
          />

          <p class="mb-2 text-base font-bold">
            {{ $t('inputs.text.access') }}
          </p>

          <input
            v-model="requestData.access_code"
            :placeholder="$t('inputs.placeholders.access')"
            name="access"
            class="InputField"
          />
        </form>

        <p v-if="error" class="error">{{ $t(`errors.${error}`) }}</p>
        <p v-else-if="success" class="success">{{ $t('success') }}</p>

        <div class="flex flex-col sm:flex-row">
          <Button @click="this.$refs.Form.submitForm()" variant="highlighted">
            {{ $t('button.submit') }}
          </Button>
        </div>
      </Form>
    </main>
  </div>
</template>
