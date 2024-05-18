<script>
import Aside from '@/components/Aside.vue';

import { PhGithubLogo, PhTranslate, PhPalette } from '@phosphor-icons/vue';

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

      <AsideButton routePath="https://github.com/fortheinternet/chalkgrades" :internal="false">
        <PhGithubLogo weight="bold" size="17px"/>
        {{ $t('button.github') }}
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

    <ChipButton :buttonText="$t('button.github')" routePath="https://github.com/fortheinternet/chalkgrades" :internal="false"/>
  </main>
</template>