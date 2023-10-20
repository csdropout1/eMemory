/* Microl Chen
microl.chen@emory.edu ~ tche284

THIS CODE WAS MY OWN WORK , IT WAS WRITTEN WITHOUT CONSULTING ANY
SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR. - Microl Chen
*/

public class BSTIndex {
    class Node {//Creates node class
        String key;
        Node left, right;
        MovieInfo data;

        Node (MovieInfo data) {//node constructor
            this.data = data;
            key = data.shortName;
            left = right = null;
        }
        MovieInfo returnData () {//ease of access for movieinfo in node
            return data;
        }
    }

    Node root;
    public BSTIndex() {//constructor
        root = null;
    }

    public MovieInfo findExact(String key) {//References private class so more arguments could be added.
        if (findExact(key, root) == null) return null;
        MovieInfo data = findExact(key, root).returnData();
        return data;
        }

    public MovieInfo findPrefix(String prefix) {//References private class so more arguments could be added.
        if (findPrefix(prefix, root) == null) return null;
        MovieInfo data = findPrefix(prefix, root).returnData();
        return data;
        }

    public void insert(MovieInfo data) {//References private class so more arguments could be added.
        root = insert(data, root);
        }

    private Node findExact(String key, Node q) {//finds the node with matching key
        if (q == null) return null; //stops errors if q is null.
        if (key.toUpperCase().compareTo(q.key.toUpperCase()) == 0) return q;//uses toUpperCase for case sensitivity.
        if (key.toUpperCase().compareTo(q.key.toUpperCase()) < 0) return findExact(key, q.left);
        if (key.toUpperCase().compareTo(q.key.toUpperCase()) > 0) return findExact(key, q.right);
        return null;
    }

    private Node findPrefix(String prefix, Node q) {//finds the node with matching key to prefix
        String remove = ""; //initiates a new string because the input string will contain *
        for (int i = 0; i < prefix.length()-1;i++) {//basically removes the * from the search string
            remove += prefix.charAt(i);
        }
        if (q == null) return null;//stops errors if q is null.
        if (remove.toUpperCase().compareTo(q.key.substring(0, remove.length()).toUpperCase()) == 0) return q;
        //uses substring to match prefix length with node keys (the short names)
        if (remove.toUpperCase().compareTo(q.key.toUpperCase()) < 0) {
            return findPrefix(prefix, q.left);
        }
        return findPrefix(prefix, q.right);

    }

    private Node insert(MovieInfo data, Node q) {//inserts a node into the BST
        if (q == null) {//initial case
            q = new Node(data);
            return q;
        }
        //compares shortNames with root keys so that the nodes can be indexed correctly.
        if (data.shortName.compareTo(q.key) < 0) {
            q.left = insert(data, q.left);

        }
        if (data.shortName.compareTo(q.key) > 0 ) {
            q.right = insert(data, q.right);
        }
        return q;

    }
}