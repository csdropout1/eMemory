import java.util.*;
public class BalancedSearchTree<K,V> {
    protected static class Node<E>{
        public E element;
        public int height=0;
        public Node<E> parent;
        public Node<E> left;
        public Node<E> right;
        public Node(E e, Node<E> above, Node<E> leftChild, Node<E> rightChild){
            element = e;
            parent = above;
            left = leftChild;
            right = rightChild;
        }
    }
    protected Comparator<K> comp;
    protected Node<Entry<K,V>> root = null;
    private int size = 0;
    public BalancedSearchTree(){comp = new DefaultComparator<K>();}
    public int size(){return size;}
    public Node<Entry<K,V>> root(){return root;}
    public int numChildren(Node<Entry<K,V>> p){
        int count = 0;
        if(p.left != null)
        count++;
        if(p.right != null)
        count++;
        return count;
    }
    public boolean isInternal(Node<Entry<K,V>> p) { return numChildren(p) > 0; }
    public boolean isExternal(Node<Entry<K,V>> p) { return numChildren(p) == 0; }
    public boolean isRoot(Node<Entry<K,V>> p) { return p == root( ); }
    public boolean isEmpty( ) { return size( ) == 0; }
    public Node<Entry<K,V>> addLeft(Node<Entry<K,V>> p, Entry<K,V> e){
       if(p.left != null)
            throw new IllegalArgumentException("p already has a left child");
        Node<Entry<K,V>> child = new Node<>(e,p,null,null);
        p.left = child;
        p.height=Math.max(1,p.height);
        size++;
        return child;
    }
    public Node<Entry<K,V>> addRight(Node<Entry<K,V>> p, Entry<K,V> e){
        if(p.right != null)
             throw new IllegalArgumentException("p already has a right child");
         Node<Entry<K,V>> child = new Node<>(e,p,null,null);
         p.right = child;
         p.height=Math.max(1,p.height);
         size++;
         return child;
     }
     public Node<Entry<K,V>> addRoot(Entry<K,V> e){
        if(!isEmpty()) throw new IllegalStateException("Tree is not empty");
        root = new Node<Entry<K,V>>(e,null,null,null);
        size = 1;
        return root;
    }
    public int height(Node<Entry<K,V>> p){
        int h = 0;
        if(p.left != null) h = Math.max(h,1+height(p.left));
        if(p.right != null) h = Math.max(h,1+height(p.right));
        return h;
    }
     /*
     public Entry<K,V> set(Node<Entry<K,V>> p, Entry<K,V> e){
        Entry<K,V> temp = p.element;
         p.element =e;
         return temp;
     }
     public void attach(Node<Entry<K,V>> p, LinkedBinaryTree<K,V> t1, LinkedBinaryTree<K,V> t2){
         if(isInternal(p)) throw new IllegalArgumentException("p must be a leaf");
         size += t1.size() + t2.size();
         if(!t1.isEmpty()){
             t1.root.parent = p;
             p.left = t1.root;
             t1.root = null; // why? -> help garbage collection.
             t1.size = 0;
         }
         if(!t2.isEmpty()){
            t2.root.parent = p;
            p.right = t2.root;
            t2.root = null; // why? -> help garbage collection.
            t2.size = 0;
        }
        
     }
     public Entry<K,V> remove(Node<Entry<K,V>> p){
        if(numChildren(p) == 2)
            throw new IllegalArgumentException("p has two children");
        Node<Entry<K,V>> child = (p.left != null ? p.left: p.right);
        if(child != null)
            child.parent = p.parent;
        if(p == root)
            root = child;
        else{
            if (p.parent.left == p) p.parent.left = child;
            if (p.parent.right == p) p.parent.right = child;
        }
        Entry<K,V> temp = p.element;
        p.parent = p;
        p.left = null;
        p.right = null;
        p.element = null;
        size--;
        return temp;
    } 
    
    public int depth(Node<Entry<K,V>> p){
        if (p==null) return -1;
        return depth(p.parent)+1;
    }
    public int height(Node<Entry<K,V>> p){
        int h = 0;
        if(p.left != null) h = Math.max(h,1+height(p.left));
        if(p.right != null) h = Math.max(h,1+height(p.right));
        return h;
    }
    public int height(Node<E> p){
        if(p==null) return -1;
        int heightLeft = height(p.left);
        int heightRight = height(p.right);
        if(heightLeft < heightRight) return heightRight + 1;
        else return heightLeft + 1;
    }*/
    public List<Node<Entry<K,V>>> traversal(String typeTraversal){
        List<Node<Entry<K,V>>> snapshot = new ArrayList<>();
        if(!isEmpty()){
            if (typeTraversal == "preorder") {preorderSubtree(root,snapshot);}
            else if (typeTraversal == "postorder") {postorderSubtree(root,snapshot);}
            else if (typeTraversal == "inorder") {inorderSubtree(root,snapshot);}
            else {breathfirst(snapshot);}
        }
        return snapshot;
    }
    protected void preorderSubtree(Node<Entry<K,V>> p, List<Node<Entry<K,V>>> snapshot) {
        snapshot.add(p);
        if (p.left != null) preorderSubtree(p.left,snapshot);
        if (p.right != null) preorderSubtree(p.right,snapshot);
    }
    protected void postorderSubtree(Node<Entry<K,V>> p, List<Node<Entry<K,V>>> snapshot) {
        if (p.left != null) postorderSubtree(p.left,snapshot);
        if (p.right != null) postorderSubtree(p.right,snapshot);
        snapshot.add(p);
    }
    protected void inorderSubtree(Node<Entry<K,V>> p, List<Node<Entry<K,V>>> snapshot) {
        if (p.left != null) inorderSubtree(p.left,snapshot);
        snapshot.add(p);
        if (p.right != null) inorderSubtree(p.right,snapshot);
        
    }
    protected void breathfirst(List<Node<Entry<K,V>>> snapshot){
        if(!isEmpty()){
            LinkedListQueue<Node<Entry<K,V>>> queue = new LinkedListQueue<>();
            queue.enqueue(root);
            
            while(!queue.isEmpty()){
                
                Node<Entry<K,V>> current = queue.dequeue();
                snapshot.add(current);
                if (current.left != null) queue.enqueue(current.left);
                if (current.right != null) queue.enqueue(current.right);
            }
        }
    }
    public Entry<K,V> remove(Node<Entry<K,V>> p){
        if(numChildren(p) == 2)
            throw new IllegalArgumentException("p has two children");
        Node<Entry<K,V>> child = (p.left != null ? p.left: p.right);
        if(child != null)
            child.parent = p.parent;
        if(p == root)
            root = child;
        else{
            if (p.parent.left == p) p.parent.left = child;
            if (p.parent.right == p) p.parent.right = child;
        }
        Entry<K,V> temp = p.element;
        p.parent = p;
        p.left = null;
        p.right = null;
        p.element = null;
        size--;
        return temp;
    }

    public void printTree(){
        

        int h = height(root);
        System.out.print(h);
        System.out.print("here");
        int length = (int) Math.pow(2,h+1)-1;
        List<K> lk = new ArrayList<K>(Collections.nCopies(length, (K) null));
        //List<K> lk = new ArrayList<>();
        formList(0,root,lk);
        for(int i = 0;i<=h;i++){
            int indexI_1 = (int) Math.pow(2,i)-1;
            int indexI = (int) Math.pow(2,i+1)-1;
            for(int j = indexI_1; j<indexI;j++){
                System.out.print(lk.get(j));
            }
            System.out.print("\n");
        }
    }
    public void formList(int index, Node<Entry<K,V>> p, List<K> lk){
        if(p.element == null) lk.set(index,null);
        else{lk.set(index,p.element.key);
        formList(index*2+1,p.left,lk);
        formList(index*2+2,p.right,lk);}
    }

    public Node<Entry<K,V>> treeSearch(Node<Entry<K,V>> p, K key){
        if(isExternal(p)) return p;
        if(comp.compare(key,p.element.key)>0) return treeSearch(p.right,key);
        else if(comp.compare(key,p.element.key)<0) return treeSearch(p.left,key);
        else return p;
    }//finally{;return p;}
    //}
    public void expandExternal(Node<Entry<K,V>> p, Entry<K,V> e){
        p.element = e;
        p.left = new Node<Entry<K,V>>(null,p,null,null);
        p.right = new Node<Entry<K,V>>(null,p,null,null);
    }
    public void insert(K key, V value){
        Node<Entry<K,V>> p = treeSearch(root,key);
        if(isExternal(p)){
            Entry<K,V> entry = new Entry<>(key,value);
            expandExternal(p,entry);
        }
        else{
            p.element.value = value;
        }
        rebalance(p);
    }
    public Node<Entry<K,V>> treeMax(Node<Entry<K,V>> p){
        if(isExternal(p.right)) return p;
        return treeMax(p.right);
    }
    public void delete(K key){
        Node<Entry<K,V>> p = treeSearch(root,key);
        if(isExternal(p)) return;
        if(isExternal(p.left) || isExternal(p.right)){
            delete01(p);
        }
        else{
            Node<Entry<K,V>> replacement = treeMax(p.left);
            p.element = replacement.element;
            delete01(replacement);
        }
        if(!isRoot(p))
            rebalance(p.parent);
    }
    public Node<Entry<K,V>> get(K key){
        Node<Entry<K,V>> p = treeSearch(root,key);
        if(isExternal(p)) return null;
        else return p;
    }
    private void delete01(Node<Entry<K,V>> p){
        Node<Entry<K,V>> leaf = (isExternal(p.left) ? p.left : p.right);
        remove(leaf);
        remove(p);
    }
    private void relink(Node<Entry<K,V>> parent, Node<Entry<K,V>> child, boolean makeLeftChild){
        child.parent = parent;
       if(makeLeftChild == true) parent.left = child;
        else
        parent.right =child;

    }
    public void rotate(Node<Entry<K,V>> p) {
    Node<Entry<K,V>> parent = p.parent;
    Node<Entry<K,V>> grandparent = parent.parent;
    //Step 1: relink c and a
    if(grandparent==null){
        root = p;
        p.parent = null;
    }    
    else relink(grandparent, p, grandparent.left == parent);

    // Step 2:
    if(parent.left==p){
        relink(parent,p.right,true);
        relink(p,parent,false);}
    else{
        relink(parent,p.left,false);
        relink(p,parent,true);
    }
    // Step 3: 
        
    }
    public Node<Entry<K,V>> restructure(Node<Entry<K,V>> p){
        Node<Entry<K,V>> parent = p.parent;
        Node<Entry<K,V>> grandparent = parent.parent;
        if((grandparent.left==parent) &&(parent.left == p)|| (grandparent.right==parent) &&(parent.right == p)){
            rotate(parent);
            return parent;
        }
        else{
            rotate(p);
            rotate(p);
            return p;
        }
    }
    
    protected void recomputeHeight(Node<Entry<K,V>> p){
        p.height = 1+Math.max(p.left.height,p.right.height);
    }
    protected Node<Entry<K,V>> tallerChildNode(Node<Entry<K,V>> p) { 
        if(height(p.left) > height(p.right)) return p.left;
        else if(height(p.left) < height(p.right)) return p.right;
        else {
            if (p.parent == null) return p.left;
            if(p == p.parent.left) return p.left;
            else return p.right;
        }
        }
    protected Node<Entry<K,V>> tallerChild(Node<Entry<K,V>> p) { 
        if(p.left.height > p.right.height) return p.left;
        else if(p.left.height < p.right.height) return p.right;
        else {
            if (p.parent == null) return p.left;
            if(p == p.parent.left) return p.left;
            else return p.right;
        }
        }


    protected void rebalance(Node<Entry<K,V>> p){
        // first tell if ancestors are unbalanced. choose the lowest one.
        // if height-unbalanced node is found, then find the tri-nodes and apply tri-node restructure.
        while(p != null){
            if(Math.abs(height(p.left)-height(p.right))>=2){
                System.out.println("executed!");
                p = restructure(tallerChildNode(tallerChildNode(p)));
            }
            p = p.parent;
        }
    }


    protected void rebalance_better_efficiency_alternative_version(Node<Entry<K,V>> p){
        int oldHeight, newHeight;
        do{
            oldHeight = p.height;
            if(Math.abs(p.left.height-p.right.height)>=2){
                System.out.println("executed!");
                p = restructure(tallerChild(tallerChild(p)));
                recomputeHeight(p.left);// these are the only nodes with heights changed.
                recomputeHeight(p.right);
            }
            recomputeHeight(p);
            newHeight = p.height;
            p = p.parent;
        } while(oldHeight != newHeight && p!= null);
    }
    protected void rebalance_better_efficiency(Node<Entry<K,V>> p){
        int oldHeight, newHeight;
        while(p != null){
            oldHeight = p.height;
            if(Math.abs(p.left.height-p.right.height)>=2){
                System.out.println("executed!");
                p = restructure(tallerChild(tallerChild(p)));
                recomputeHeight(p.left);// these are the only nodes with heights changed.
                recomputeHeight(p.right);
            }
            recomputeHeight(p);
            newHeight = p.height;
            if(oldHeight == newHeight) break;
            p = p.parent;
        }
    }
}


