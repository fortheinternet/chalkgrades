<script>
import { PhGithubLogo, PhTranslate, PhPalette, PhCalculator, PhCloudCheck, PhUser, PhUserPlus, PhHouse } from '@phosphor-icons/vue';

import ChipButton from '@/components/ChipButton.vue';
import AsideButton from '@/components/AsideButton.vue';
import ToggleLocale from '@/components/ToggleLocale.vue';
import ToggleTheme from '@/components/ToggleTheme.vue';

export default {
  name: 'LoginView',
  components: {
    // Phosphor Icons
    PhGithubLogo,
    PhTranslate,
    PhPalette,
    PhCalculator,
    PhCloudCheck,
    PhUser,
    PhUserPlus,
    PhHouse,

    // UI elements
    ChipButton,
    AsideButton,
    ToggleLocale,
    ToggleTheme
  },
  created() {
    document.title = this.$t('title.Signup')
  }
};
</script>


<template>
  <aside>
    <div>
      <AsideButton routePath="/" :internal="true">
        <PhHouse weight="bold" size="17px"/>
        {{ $t('button.home') }}
      </AsideButton>

      <AsideButton routePath="/login" :internal="true">
        <PhUser weight="bold" size="17px"/>
        {{ $t('button.login') }}
      </AsideButton>

      <AsideButton routePath="/signup" :internal="true">
        <PhUserPlus weight="bold" size="17px"/>
        <span class="font-bold"> {{ $t('button.signup') }} </span>
      </AsideButton>

      <div class="divider"></div>
      
      <AsideButton routePath="https://github.com/fortheinternet/chalkgrades" :internal="false">
        <PhGithubLogo weight="bold" size="17px"/>
        {{ $t('button.github') }}
      </AsideButton>

      <AsideButton routePath="https://regex101.com" :internal="false">
        <PhCalculator weight="bold" size="17px"/>
        {{ $t('button.regex-generator') }}
      </AsideButton>

      <AsideButton routePath="https://fortheinternet.notion.site/API-Documentation-WIP-be3e672768d243aa855209b4f6e475bb?pvs=4" :internal="false">
        <PhCloudCheck weight="bold" size="17px"/>
        {{ $t('button.api-docs') }}
      </AsideButton>
    </div>
    <div>
      <ToggleLocale view="Signup">
        <PhTranslate weight="bold" size="17px"/>
        {{ $t('button.changelang') }}
      </ToggleLocale>

      <ToggleTheme>
        <PhPalette weight="bold" size="17px"/>
        {{ $t('button.changetheme') }}
      </ToggleTheme>
    </div>
  </aside>
  <main>
    <article>
      <h4>{{ $t('text.heading.signup-1') }}</h4>
      <p class="dark:text-opacity-55 text-opacity-55 dark:text-white text-black">{{ $t('text.paragraph.signup-1') }}</p>
    </article>
  </main>
</template>