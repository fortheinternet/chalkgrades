<script>
  // Phosphor Icons
  import {
    PhGithubLogo,
    PhCalculator,
    PhCloudCheck,
    PhUser,
    PhHouse
  } from '@phosphor-icons/vue'

  // UI elements
  import AsideButton from '@/components/AsideButton.vue'
  import ChangeLocale from '@/components/ChangeLocale.vue'
  import ToggleTheme from '@/components/ToggleTheme.vue'

  export default {
    components: {
      // Phosphor Icons
      PhGithubLogo,
      PhCalculator,
      PhCloudCheck,
      PhUser,
      PhHouse,

      // UI elements
      AsideButton,
      ChangeLocale,
      ToggleTheme
    },
    props: {
      view: ''
    }
  }
</script>

<template>
  <aside class="left-aside">
    <div>
      <div>
        <AsideButton routePath="/" :internal="true">
          <PhHouse v-if="view == 'Home'" weight="fill" size="17px" />
          <PhHouse v-else weight="bold" size="17px" />

          <div :class="{ 'font-bold': view == 'Home' }">
            {{ $t('button.home') }}
          </div>
        </AsideButton>

        <AsideButton routePath="/login" :internal="true">
          <PhUser v-if="view == 'Login'" weight="fill" size="17px" />
          <PhUser v-else weight="bold" size="17px" />

          <div :class="{ 'font-bold': view == 'Login' }">
            {{ $t('button.login') }}
          </div>
        </AsideButton>
      </div>
      <div class="divider my-8"></div>
      <div>
        <AsideButton
          routePath="https://github.com/fortheinternet/chalkgrades"
          :internal="false"
        >
          <PhGithubLogo weight="bold" size="17px" />
          {{ $t('button.github') }}
        </AsideButton>

        <AsideButton routePath="https://regex101.com" :internal="false">
          <PhCalculator weight="bold" size="17px" />
          {{ $t('button.regex-generator') }}
        </AsideButton>

        <AsideButton
          routePath="https://fortheinternet.notion.site/API-Documentation-WIP-be3e672768d243aa855209b4f6e475bb?pvs=4"
          :internal="false"
        >
          <PhCloudCheck weight="bold" size="17px" />
          {{ $t('button.api-docs') }}
        </AsideButton>
      </div>
    </div>
    <div>
      <div>
        <ChangeLocale :view />
        <ToggleTheme />
      </div>
    </div>
  </aside>
</template>
