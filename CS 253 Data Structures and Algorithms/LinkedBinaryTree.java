import java.util.*;
public class LinkedBinaryTree<K,V> {
    protected static class Node<E>{
        public E element;
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
    public LinkedBinaryTree(){comp = new DefaultComparator<K>();}
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
        size++;
        return child;
    }
    public Node<Entry<K,V>> addRight(Node<Entry<K,V>> p, Entry<K,V> e){
        if(p.right != null)
             throw new IllegalArgumentException("p already has a right child");
         Node<Entry<K,V>> child = new Node<>(e,p,null,null);
         p.right = child;
         size++;
         return child;
     }
     public Node<Entry<K,V>> addRoot(Entry<K,V> e){
        if(!isEmpty()) throw new IllegalStateException("Tree is not empty");
        root = new Node<Entry<K,V>>(e,null,null,null);
        size = 1;
        return root;
    }
    public int depth(Node<Entry<K,V>> p){
        if (p.parent==null) return 0;
        return depth(p.parent)+1;
    }

    public List<Node<Entry<K,V>>> traversal(String typeTraversal){
        List<Node<Entry<K,V>>> record = new ArrayList<>();
        if(!isEmpty()){
            if (typeTraversal == "preorder") {preorderSubtree(root,record);}
            else if (typeTraversal == "postorder") {postorderSubtree(root,record);}
            else if (typeTraversal == "inorder") {inorderSubtree(root,record);}
            else {breathfirst(record);}
        }
        return record;
    }
    protected void breathfirst(List<Node<Entry<K,V>>> record){
        if(root == null) return;
        LinkedListQueue<Node<Entry<K,V>>> queue = new LinkedListQueue<>();
        queue.enqueue(root);
        while(queue.isEmpty() == false){
            Node<Entry<K,V>> curNode = queue.dequeue();
            if(curNode.left != null) queue.enqueue(curNode.left);
            if(curNode.right != null) queue.enqueue(curNode.right);
        }
    }

    protected void preorderSubtree(Node<Entry<K,V>> p, List<Node<Entry<K,V>>> record) {
        record.add(p);//visit root
        //go into left child's branch
        if(p.left != null) preorderSubtree(p.left,record);
        //go into right child's branch
        if(p.right != null) preorderSubtree(p.right,record);
    }
    protected void postorderSubtree(Node<Entry<K,V>> p, List<Node<Entry<K,V>>> record) {
        // leftsubtree
        if(p.left != null)  postorderSubtree(p.left,record);
        // rightsubtree
        if(p.right != null) postorderSubtree(p.right, record);
        // root
        record.add(p);
    }
    protected void inorderSubtree(Node<Entry<K,V>> p, List<Node<Entry<K,V>>> record) {
        if(p.left != null) inorderSubtree(p.left,record);
        record.add(p);
        if(p.right != null) inorderSubtree(p.right, record);
    }
    public int height(Node<Entry<K,V>> p){
        if(numChildren(p)==0) return 0;
        int maxHeight = 0;
        if(p.left != null) maxHeight = height(p.left);
        if(p.right != null){
            int rightHeight = height(p.right);
            if(maxHeight <rightHeight){
                maxHeight = rightHeight;
            }
        } 
        return maxHeight+1;
    }
    private void delete01(Node<Entry<K,V>> p){
        Node<Entry<K,V>> leaf = (isExternal(p.left) ? p.left : p.right);
        remove(leaf);
        remove(p);
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
    }
public void delete_splay(K key){
        Node<Entry<K,V>> p = treeSearch(root,key);
        if(isExternal(p)) return;
        Node<Entry<K,V>> parent = p.parent;
        if(isExternal(p.left) || isExternal(p.right)){
            delete01(p);
        }
        else{
            Node<Entry<K,V>> replacement = treeMax(p.left);
            p.element = replacement.element;
            delete01(replacement);
        }
        System.out.println(p.element);
        System.out.println(p.parent);
        if (parent != null) splay(parent);
        
    }
    
    public Node<Entry<K,V>> treeSearch(Node<Entry<K,V>> p, K key){
        // terminal: 
        if(isExternal(p)) return p;
        // key > root's key
        if(comp.compare(key,p.element.key) > 0) {
           return  treeSearch(p.right,key);
        }
        // key < root's key
        else if(comp.compare(key, p.element.key) < 0) {
            return treeSearch(p.left,key);
        }
        // key == root's key
        else {
            return p;
        }
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
}
    public void splay(Node<Entry<K,V>> p){
while(!isRoot(p)){
    if(isRoot(p.parent)){
        rotate(p);
    }
    else{
        //straight-line (aka zig-zig)
        if((p==p.parent.right)&&(p.parent.parent.right==p.parent)||(p==p.parent.left)&&(p.parent.parent.left==p.parent))
        {
            rotate(p.parent);
            rotate(p);
        }
    else{// zig-zag
        rotate(p);
        rotate(p);
    }

        
    }







}

















    }















    public void printTree(){
        
        List<Node<Entry<K,V>>> currentList = traversal("inorder");
        
        for (Node<Entry<K,V>> c: currentList){
            if(c.element != null) System.out.print(c.element.key);
            else System.out.print(c.element);
        }
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
    }
    public void insert_splay(K key, V value){
        Node<Entry<K,V>> p = treeSearch(root,key);
        if(isExternal(p)){
            Entry<K,V> entry = new Entry<>(key,value);
            expandExternal(p,entry);
        }
        else{
            p.element.value = value;
        }
        splay(p);
    }
    public Node<Entry<K,V>> treeMax(Node<Entry<K,V>> p){
        if(isExternal(p.right)) return p;
        return treeMax(p.right);
    }
    
    public Node<Entry<K,V>> get(K key){
        Node<Entry<K,V>> p = treeSearch(root,key);
        if(isExternal(p)) return null;
        else return p;
    }
    public Node<Entry<K,V>> get_splay(K key){
        Node<Entry<K,V>> p = treeSearch(root,key);
        if(isExternal(p)) {
            if(p.parent != null) splay(p.parent);
            return null;}
        else {
            splay(p);
            return p;}

    }
    public void attach(Node<Entry<K,V>> p, LinkedBinaryTree<K,V> t1, LinkedBinaryTree<K,V> t2){
        if (isInternal(p)) throw new IllegalArgumentException("p must be a leaf");
        if(t1 != null){
            p.left = t1.root;
            t1.root = p;
            size += t1.size;
        }
        if(t2 != null){
            p.right = t2.root;
            t2.root = p;
            size += t2.size;
        }
    }
    public Entry<K,V> remove(Node<Entry<K,V>> p){
        // if two children
        if(numChildren(p)==2) throw new IllegalArgumentException("two children!");

        // operate on child
        // define a child, to hold the only one child, if no child, then it is null.
        Node<Entry<K,V>> child = p.left;
        if(p.left == null){child = p.right;}
        if(child != null) child.parent = p.parent;
        // operate on p's parent
        if(p.parent == null) root = child;
        else{
            // whether update parent.left or parent.right?
            if(p==p.parent.left){
                p.parent.left = child;
            }
            else{
                p.parent.right = child;
            }
        }
        
        p.parent = null;
        p.left = null;
        p.right = null;
        p.element = null;


        return null;
    }
   

    public static void main(String[] args) {
        LinkedBinaryTree<Integer,String> test = new LinkedBinaryTree<>();
        Node<Entry<Integer,String>> root = test.addRoot(new Entry<Integer,String>(8,"a"));
        Node<Entry<Integer,String>> n1 = test.addLeft(root, new Entry<Integer,String>(5,"b"));
        Node<Entry<Integer,String>> n2 = test.addRight(root, new Entry<Integer,String>(13,"d"));
        Node<Entry<Integer,String>> n3 = test.addLeft(n2, new Entry<Integer,String>(10,"c"));
        Node<Entry<Integer,String>> n4 = test.addRight(n2, new Entry<Integer,String>(18,"e"));
        Node<Entry<Integer,String>> n5 = test.addLeft(n3, new Entry<Integer,String>(9,"f"));
        Node<Entry<Integer,String>> n6 = test.addRight(n3, new Entry<Integer,String>(12,"g"));
        Node<Entry<Integer,String>> n7 = test.addLeft(n4, new Entry<Integer,String>(15,"h"));
        Node<Entry<Integer,String>> n8 = test.addLeft(n6, new Entry<Integer,String>(11,"i"));
        // test.addLeft(n1, null);
        // test.addRight(n1, null);
        // test.addLeft(n5, null);
        // test.addRight(n5, null);
        // test.addLeft(n8, null);
        // test.addRight(n8, null);
        // test.addRight(n6, null);
        // test.addLeft(n7, null);
        // test.addRight(n7, null);
        // test.addRight(n4, null);
        System.out.println(test.height(test.root));
        System.out.println(test.depth(test.root));
    }
}