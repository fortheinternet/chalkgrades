<template>
    <aside>
        <slot></slot>
    </aside>
</template>

<style>
    aside {
        @apply bg-black dark:bg-white bg-opacity-5 dark:bg-opacity-[1%] border-r-[1px] border-solid dark:border-white border-black dark:border-opacity-5 border-opacity-5 md:flex flex-col justify-between whitespace-nowrap select-none items-start lg:w-[450px] md:w-1/2 w-full h-full fixed p-8 hidden overflow-y-auto
    }
</style>