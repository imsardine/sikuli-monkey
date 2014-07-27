sikuli-monkey
=============

An extension of [Sikuli](http://www.sikuli.org/) that enables running scripts against real Android devices without rooting them.

We all knows object-based (or component-based) testing tools are preferred, but at times image-baased tools are needed as a complementary or fallback solution. Sikuli is a great image-based testing tool for many kinds of applications, if (and only if) users can interact with them on the desktop. 

For the problem of Sikuli on Android devices, there exist some approaches:

 * Emulators
 * VNC servers, and require root

These two approaches rely on the fact that Sikuli can see the app and control it directly or indirectly with keystrokes and mouse operations.

For some reason, if they are not applicable to your application under test, here is another option for you. 

sikuli-monkey is a combination of [monkeyrunner](http://developer.android.com/tools/help/monkeyrunner_concepts.html) and an extended version of Sikuli.

 * monkeyrunner - for capturing screenshots and sending keyboard and touch events.
 * Siklui - as a scripting environment, and for identifying UI components via image recognition.

The concept is really simple and is inspired by an extension to Sikuli called [android-robot](https://github.com/sikuli/sikuli/tree/develop/extensions/android-robot). That is extending Sikuli and adding a layer of redirection/delegation. For example:

 * When Sikuli needs a screenshot, delegate it to monkeyrunner and take a screenshot from the device.
 * When Sikuli performs an action, delegate the call to monkeyrunner and perform it on the device.

To see siklui-monkey in action, watch the video below:

<blockquote>
<a href="http://www.youtube.com/watch?feature=player_embedded&v=g46T3-zmKdE" target="_blank">
  <img src="http://img.youtube.com/vi/g46T3-zmKdE/0.jpg" alt="Sikuli on Android (no root)" width="240" border="0" />
</a>
</blockquote>

