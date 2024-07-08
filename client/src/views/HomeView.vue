<script>
  // Layouts
  import LandingLeft from '@/layouts/LandingLeft.vue'

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
    <article
      class="flex aspect-[10/5] w-full flex-col items-center justify-center rounded-lg"
    >
      <h4>{{ $t('text.heading.landing-1') }}</h4>
      <p class="subtext mb-10">{{ $t('text.paragraph.landing-1') }}</p>
      <div class="button-row">
        <Button routePath="/login" :internal="true" :highlighted="true">
          {{ $t('button.login') }}
        </Button>
        <Button
          routePath="https://github.com/fortheinternet/chalkgrades"
          :internal="false"
          :highlighted="false"
        >
          {{ $t('button.github') }}
        </Button>
      </div>
    </article>

    <article>
      <h5>{{ $t('text.heading.latest-updates') }}</h5>
      <p>{{ $t('text.paragraph.latest-changes') }}</p>
    </article>

    <Divider />

    <article>
      <h6 class="xl:mb-1">{{ $t('text.heading.landing-2') }}</h6>
      <p class="xl:m-0">{{ $t('text.paragraph.landing-2') }}</p>
    </article>

    <article>
      <h6 class="xl:mb-1">{{ $t('text.heading.landing-3') }}</h6>
      <p class="xl:m-0">{{ $t('text.paragraph.landing-3') }}</p>
    </article>

    <article>
      <h6 class="xl:mb-1">{{ $t('text.heading.landing-4') }}</h6>
      <p class="xl:m-0">{{ $t('text.paragraph.landing-4') }}</p>
    </article>
  </main>
</template>
