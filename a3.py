# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software
# Libraries in Python

# Replace the following placeholders with your information.

# Jiayi Zhu
# jzhu42@uci.edu
# 94623196

"""Main GUI and controller for A3 Direct Messaging Chat."""
# pylint: disable=too-many-instance-attributes,
# too-many-arguments, too-many-positional-arguments
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from ds_messenger import DirectMessenger
import notebook


class Body(tk.Frame):
    """Main UI body showing contacts and messages."""

    def __init__(self, root: tk.Tk,
                 recipient_selected_callback=None) -> None:
        """
        Initializes the Body frame which contains the
        contact list and message editor.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def get_contacts(self):
        """get the contact list."""
        return self._contacts

    def node_select(self) -> None:
        """Handles contact selection from the contact list."""
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str) -> None:
        """Adds a contact to the contact list if not already present."""
        if contact in self._contacts:
            return
        self._contacts.append(contact)
        contact_id = len(self._contacts) - 1
        self._insert_contact_tree(contact_id, contact)

    def _insert_contact_tree(self, contact_id, contact: str) -> None:
        """Inserts a contact into the Treeview widget."""
        if len(contact) > 25:
            contact = contact[:24] + "..."  # for debugging
        self.posts_tree.insert('', contact_id, contact_id, text=contact)

    def insert_user_message(self, message: str) -> None:
        """Displays a user's message in the message display area."""
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str) -> None:
        """Displays a received message in the message display area."""
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """Returns the current text input from the message entry box."""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str) -> None:
        """Sets the text in the message entry box."""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self) -> None:
        """Draws the GUI layout for the Body section."""
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """Footer with send button and status."""

    def __init__(self, root: tk.Tk,
                 send_callback=None) -> None:
        """
        Initializes the footer frame containing
        the send button and status label.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self) -> None:
        """Trigger the send callback when the Send button is clicked."""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self) -> None:
        """Draw the send button and status label."""
        save_button = tk.Button(master=self, text="Send",
                                width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
class NewContactDialog(tk.simpledialog.Dialog):
    """Dialog for server, username, password input."""
    def __init__(self, root: tk.Tk, title: str = None, user: str = None,
                 pwd: str = None, server: str = None) -> None:
        """
        Dialog for configuring DS server connection details.
        """
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, master) -> None:
        """Draws the form fields for server, username, and password."""
        frame = master
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self) -> None:
        """Stores the entered configuration when dialog is confirmed."""
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """Main application class managing GUI and logic."""

    def __init__(self, root: tk.Tk) -> None:
        """
        Initializes the main application GUI frame, sets up
        initial state and draws layout.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.direct_messenger = None
        self.notebook = notebook.Notebook(
            username=self.username, password=self.password)
        self._draw()

    def _load_contacts(self) -> None:
        """Loads contacts from notebook file and displays them in the GUI."""
        self.notebook.load(f"{self.username}.json")
        contacts = self.notebook.get_contacts()
        for contact in contacts:
            if contact != self.username:
                self.body.insert_contact(contact)

    def _load_messages(self) -> None:
        """(Placeholder) Attempts to load messages from file, if any."""
        try:
            self.notebook.load(f"{self.username}.json")
        except Exception:   # pylint: disable=broad-exception-caught
            pass

    def send_message(self) -> None:
        """
        Sends a message to the selected recipient.
        Validates input and updates both GUI and local notebook.
        """
        if not self.direct_messenger:
            tk.messagebox.showerror(
                "Error", "Please configure the DS server first.")
            return

        if not self.recipient:
            tk.messagebox.showerror(
                "Error", "Please select a contact to send message.")
            return

        message = self.body.get_text_entry()

        if not message.strip():
            tk.messagebox.showwarning("Warning", "Cannot send empty message.")
            return

        success = self.direct_messenger.send(message, self.recipient)

        if success:
            self.body.insert_user_message(f"You: {message}")
            self.body.set_text_entry("")
            self._sync_server_messages()
        else:
            tk.messagebox.showerror("Error", "Message failed to send.")

    def add_contact(self) -> None:
        """Prompts user to add a contact and saves it to the notebook."""
        contact = tk.simpledialog.askstring(
            "Add Contact", "Enter the new contact's username:")
        if contact != self.username:
            self.body.insert_contact(contact)
            self.notebook.add_contact(contact)
            self.notebook.save(f"{self.username}.json")

    def recipient_selected(self, recipient) -> None:
        """Loads and displays messages with the selected contact."""
        self.recipient = recipient
        self.body.entry_editor.delete(1.0, tk.END)
        messages = self.notebook.get_messages()
        for msg in messages:
            if ((msg.sender == self.username and
                 msg.recipient == recipient) or
                (msg.sender == recipient and
                 msg.recipient == self.username)):
                if msg.sender == self.username:
                    self.body.insert_user_message(f"You: {msg.message}")
                else:
                    self.body.insert_contact_message(
                        f"{msg.sender}: {msg.message}")

    def _sync_server_messages(self) -> None:
        """Fetches all messages from server and updates notebook and UI."""
        if self.direct_messenger is None:
            return

        messages = self.direct_messenger.retrieve_all()

        for msg in messages:
            self.notebook.add_message(msg)

        self.notebook.save(f"{self.username}.json")

    def configure_server(self) -> None:
        """Launches dialog to configure server and
        authenticates via DirectMessenger."""
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        try:
            self.direct_messenger = DirectMessenger(
                dsuserver=self.server,
                username=self.username,
                password=self.password
            )
        except Exception:  # pylint: disable=broad-exception-caught
            self.direct_messenger = None

        path = f"{self.username}.json"
        if Path(path).exists():
            self.notebook = notebook.Notebook(
                username=self.username, password=self.password)
            self.notebook.load(path)
        else:
            self.notebook = notebook.Notebook(
                username=self.username, password=self.password)
            self.notebook.save(path)

        self._sync_server_messages()
        self._load_contacts()
        self._load_messages()

    def publish(self, message: str) -> None:
        """(Unused stub) Simulates publishing a message."""
        self.body.insert_user_message(f"You: {message}")

    def check_new(self) -> None:
        """
        Periodically checks for new messages.
        Adds new contacts and messages to UI and notebook if needed.
        """
        if self.direct_messenger is not None:
            messages = self.direct_messenger.retrieve_new()
            for msg in messages:
                sender = msg.sender
                if sender not in self.body.get_contacts():
                    self.body.insert_contact(sender)
                    self.notebook.add_contact(sender)
                self.notebook.add_message(msg)
                if self.recipient == sender:
                    self.body.insert_contact_message(
                        f"{sender}: {msg.message}")
            self.notebook.save(f"{self.username}.json")
        self.root.after(2000, self.check_new)

    def _draw(self) -> None:
        """Draws the full UI layout with menus, body, and footer."""
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    user_id = main.after(2000, app.check_new)
    print(user_id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
