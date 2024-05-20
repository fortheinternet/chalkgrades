<script>
import Aside from '@/components/Aside.vue';

import { PhGithubLogo, PhTranslate, PhPalette, PhCalculator, PhCloudCheck, PhUser } from '@phosphor-icons/vue';

import ChipButton from '@/components/ChipButton.vue';
import AsideButton from '@/components/AsideButton.vue';
import ToggleLocale from '@/components/ToggleLocale.vue';
import ToggleTheme from '@/components/ToggleTheme.vue';


export default {
  name: 'HomeView',
  components: {
    // Phosphor Icons
    PhGithubLogo,
    PhTranslate,
    PhPalette,
    PhCalculator,
    PhCloudCheck,
    PhUser,

    // UI elements
    Aside,
    ChipButton,
    AsideButton,
    ToggleLocale,
    ToggleTheme
  },
  created() {
    document.title = this.$t('title.Home')
  }
};
</script>


<template>
  <Aside>
    <div>
      <AsideButton routePath="/login" :internal="true">
        <PhUser weight="bold" size="17px"/>
        {{ $t('button.login') }}
      </AsideButton>

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
      <ToggleLocale>
        <PhTranslate weight="bold" size="17px"/>
        {{ $t('button.changelang') }}
      </ToggleLocale>

      <ToggleTheme>
        <PhPalette weight="bold" size="17px"/>
        {{ $t('button.changetheme') }}
      </ToggleTheme>
    </div>
  </Aside>
  <main>
    <article>
      <h4>{{ $t('text.heading.landing-1') }}</h4>
      <p class="dark:text-opacity-55 text-opacity-55 dark:text-white text-black">{{ $t('text.paragraph.landing-1') }}</p>
    </article>

    <ChipButton routePath="/login" :internal="true" :highlighted="true">{{ $t('button.login') }}</ChipButton>
    <ChipButton routePath="https://github.com/fortheinternet/chalkgrades" :internal="false" :highlighted="false">{{ $t('button.github') }}</ChipButton>
  </main>
</template>