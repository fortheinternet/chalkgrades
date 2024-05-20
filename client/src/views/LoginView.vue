<script>
import Aside from '@/components/Aside.vue';

import { PhGithubLogo, PhTranslate, PhPalette, PhCalculator, PhCloudCheck, PhUser, PhHouse } from '@phosphor-icons/vue';

import ChipButton from '@/components/ChipButton.vue';
import AsideButton from '@/components/AsideButton.vue';
import ToggleLocale from '@/components/ToggleLocale.vue';
import ToggleTheme from '@/components/ToggleTheme.vue';


export default {
  name: 'LoginView',
  components: {
    // Phosphor Icons
    PhTranslate,
    PhPalette,
    PhHouse,

    // UI elements
    Aside,
    ChipButton,
    AsideButton,
    ToggleLocale,
    ToggleTheme
  },
  created() {
    document.title = this.$t('title.Login')
  }
};
</script>


<template>
  <Aside>
    <div>
      <AsideButton routePath="/" :internal="true">
        <PhHouse weight="bold" size="17px"/>
        {{ $t('button.home') }}
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
      <h4>{{ $t('text.heading.login-1') }}</h4>
      <p class="dark:text-opacity-55 text-opacity-55 dark:text-white text-black">{{ $t('text.paragraph.login-1') }}</p>
    </article>
  </main>
</template>