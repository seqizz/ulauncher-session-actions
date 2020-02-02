from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import os

class SessionActionsExtension(Extension):

    def __init__(self):
        super(SessionActionsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        options = [
            'logout',
            'restart',
            'reboot',
            'shutdown',
            'halt',
            'suspend',
            'sleep',
            'hibernate'
        ]
        reboot_command = extension.preferences['reboot_command']
        shutdown_command = extension.preferences['shutdown_command']
        logout_command = extension.preferences['logout_command']
        suspend_command = extension.preferences['suspend_command']
        hibernate_command = extension.preferences['hibernate_command']
        myList = event.query.split(" ")
        if len(myList) == 1:
            items.append(
                ExtensionResultItem(
                    icon='images/reboot.png',
                    name='Reboot',
                    description='Restart computer',
                    on_enter=RunScriptAction(reboot_command, None)
                )
            )
            items.append(
                ExtensionResultItem(
                    icon='images/shutdown.png',
                    name='Shutdown',
                    description='Power off computer',
                    on_enter=RunScriptAction(shutdown_command, None)
                )
            )
            items.append(
                ExtensionResultItem(
                    icon='images/logout.png',
                    name='Logout',
                    description='Logout from session',
                    on_enter=RunScriptAction(logout_command, None)
                )
            )
            items.append(
                ExtensionResultItem(
                    icon='images/suspend.png',
                    name='Suspend',
                    description='Trigger sleep mode',
                    on_enter=RunScriptAction(suspend_command, None)
                )
            )
            items.append(
                ExtensionResultItem(
                    icon='images/hibernate.png',
                    name='Hibernate',
                    description='Suspend to disk',
                    on_enter=RunScriptAction(hibernate_command, None)
                )
            )

            return RenderResultListAction(items)
        else:
            myQuery = myList[1]
            included = []
            for option in options:
                if myQuery in option:
                    if option in ['shutdown', 'halt'] and 'shutdown' not in included:
                        items.append(
                            ExtensionResultItem(
                                icon='images/shutdown.png',
                                name='Shutdown',
                                description='Power off computer',
                                on_enter=RunScriptAction(shutdown_command, None)
                            )
                        )
                        included.append('shutdown')
                    elif option in ['restart', 'reboot'] and 'reboot' not in included:
                        items.append(
                            ExtensionResultItem(
                                icon='images/reboot.png',
                                name='Reboot',
                                description='Restart computer',
                                on_enter=RunScriptAction(reboot_command, None)
                            )
                        )
                        included.append('reboot')
                    elif option in ['suspend', 'sleep'] and 'suspend' not in included:
                        items.append(
                            ExtensionResultItem(
                                icon='images/suspend.png',
                                name='Suspend',
                                description='Trigger sleep mode',
                                on_enter=RunScriptAction(suspend_command, None)
                            )
                        )
                        included.append('suspend')
                    elif option in ['logout']:
                        items.append(
                            ExtensionResultItem(
                                icon='images/logout.png',
                                name='Logout',
                                description='Logout from session',
                                on_enter=RunScriptAction(logout_command, None)
                            )
                        )
                    elif option in ['hibernate']:
                        items.append(
                            ExtensionResultItem(
                                icon='images/hibernate.png',
                                name='Hibernate',
                                description='Suspend to disk',
                                on_enter=RunScriptAction(hibernate_command, None)
                            )
                        )

            return RenderResultListAction(items)

if __name__ == '__main__':
    SessionActionsExtension().run()
