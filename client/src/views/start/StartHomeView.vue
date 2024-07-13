<script>
  // Layouts
  import LandingLeft from '@/layouts/StartLayout.vue'

  // Phosphor Icons
  import {
    PhUsersThree,
    PhPaperPlaneTilt,
    PhGithubLogo
  } from '@phosphor-icons/vue'

  // UI elements
  import Button from '@/components/Button.vue'
  import Divider from '@/components/Divider.vue'

  export default {
    components: {
      // Layouts
      LandingLeft,

      // Phosphor Icons
      PhUsersThree,
      PhPaperPlaneTilt,
      PhGithubLogo,

      // UI elements
      Button,
      Divider
    },
    created() {
      document.title = this.$t('title.Home')

      if (localStorage.getItem('token')) {
        this.$router.push('/dashboard')
      }
    }
  }
</script>

<template>
  <LandingLeft view="Home" />
  <main>
    <article>
      <h4>{{ $t('text.heading.landing-1') }}</h4>
      <p class="subtext mb-10">{{ $t('text.paragraph.landing-1') }}</p>
    </article>
    <article>
      <div class="button-row">
        <Button routePath="/login" variant="highlighted">
          {{ $t('button.login') }}
        </Button>
        <Button routePath="https://github.com/fortheinternet/chalkgrades">
          {{ $t('button.github') }}
        </Button>
      </div>
    </article>

    <Divider />

    <article>
      <h5>{{ $t('text.heading.latest-updates') }}</h5>
      <p>{{ $t('text.paragraph.latest-changes') }}</p>
    </article>
  </main>
</template>
